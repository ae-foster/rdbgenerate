# This is a Python .rdb generator inspired by https://github.com/antirez/redis/blob/unstable/src/rdb.c
#
# Copyright (c) 2009-2012, Salvatore Sanfilippo <antirez at gmail dot com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of Redis nor the names of its contributors may be used
#     to endorse or promote products derived from this software without
#     specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

from __future__ import annotations

import os
from types import TracebackType
from typing import TYPE_CHECKING, BinaryIO, Collection, Final, Mapping, Sequence, Set, Union

import rdbgenerate.constants as const
from rdbgenerate.crc64 import START_CRC, crc64

if TYPE_CHECKING:
    REDIS_DATA_TYPES = Union[bytes, Collection[bytes], Mapping[bytes, bytes]]
    REDIS_DB_TYPE = dict[bytes, REDIS_DATA_TYPES]


DEFAULT_REDIS_VERSION: Final[int] = 7


def rdb_generate(
    path: Union[str, bytes, os.PathLike[str], os.PathLike[bytes]],
    redis_version: int = DEFAULT_REDIS_VERSION,
    **dbn_to_dict: REDIS_DB_TYPE,
) -> None:
    """Converts dictionaries into a redis rdb file"""
    with open(path, "wb") as f:
        rdb_generate_io(f, redis_version=redis_version, **dbn_to_dict)


def rdb_generate_io(
    bytesio: BinaryIO,
    redis_version: int = DEFAULT_REDIS_VERSION,
    **dbn_to_dict: REDIS_DB_TYPE,
) -> None:
    with RDBWriter(bytesio, redis_version=redis_version) as writer:
        for dbn, dct in dbn_to_dict.items():
            if not dbn.startswith("db") or not dbn[2:].isnumeric():
                raise ValueError("Database numbers should take the form db0")
            n = int(dbn[2:])
            if dct:
                writer.write_db(n, dct)


class RDBWriter:
    def __init__(
        self, bytesio: BinaryIO, redis_version: int = DEFAULT_REDIS_VERSION
    ) -> None:
        self.bytesio: BinaryIO = bytesio
        self.crc: int = START_CRC
        self.redis_version: int = redis_version

    def __enter__(self) -> "RDBWriter":
        self._write_header()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._write_eof()

    def write_db(self, db: int, dct: REDIS_DB_TYPE | None = None) -> None:
        self._write_bytes(const.RDB_OPCODE_SELECTDB + bytes([db]))
        if not dct:
            return
        for key, value in dct.items():
            self.write_fragment(key, value)

    def _write_bytes(self, inp: bytes) -> None:
        self.crc = crc64(inp, crc=self.crc)
        self.bytesio.write(inp)

    def write_fragment(self, key: bytes, value: REDIS_DATA_TYPES) -> None:
        bytes_key = convert_string(key)

        # Select data type
        if isinstance(value, bytes):
            typecode = const.RDB_TYPE_STRING
            bytes_value = convert_string(value)
        elif isinstance(value, Set):
            typecode = const.RDB_TYPE_SET
            bytes_value = convert_list(value)
        elif isinstance(value, Mapping):
            typecode = const.RDB_TYPE_HASH
            bytes_value = convert_hash(value)
        elif isinstance(value, Sequence):
            typecode = const.RDB_TYPE_LIST
            bytes_value = convert_list(value)  # type: ignore[arg-type]
        else:
            raise ValueError("Invalid value in dict {}".format(value))

        self._write_bytes(typecode + bytes_key + bytes_value)

    def _write_header(self) -> None:
        self._write_bytes(b"REDIS" + format(self.redis_version, "04d").encode("ascii"))

    def _write_eof(self) -> None:
        self._write_bytes(const.RDB_OPCODE_EOF)
        self.bytesio.write(self.crc.to_bytes(8, byteorder="little"))


def convert_string(string: bytes) -> bytes:
    assert isinstance(string, bytes), "Use Python bytes objects to represent strings"
    length = encode_length(len(string))
    return length + string


def encode_length(length: int) -> bytes:
    if length <= 63:
        return length.to_bytes(1, byteorder="big")
    elif length <= 16383:
        return bytes([64 + length // 256, length % 256])
    else:
        return b"\x80" + length.to_bytes(4, byteorder="big")


def convert_list(lst: Collection[bytes]) -> bytes:
    length = encode_length(len(lst))
    return length + b"".join([convert_string(s) for s in lst])


def convert_hash(hash_obj: Mapping[bytes, bytes]) -> bytes:
    length = encode_length(len(hash_obj))
    return length + b"".join(
        [convert_string(k) + convert_string(v) for k, v in hash_obj.items()]
    )
