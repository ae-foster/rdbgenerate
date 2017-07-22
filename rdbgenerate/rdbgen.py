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

from rdbgenerate.crc64 import crc64
import rdbgenerate.constants as const


def rdb_generate(path, redis_version=7, **dbn_to_dict):
    """Converts dictionaries into a redis rdb file"""
    with open(path, 'wb') as f:
        rdb_generate_io(f, redis_version=redis_version, **dbn_to_dict)


def rdb_generate_io(bytesio, redis_version=7, **dbn_to_dict):
    data_bytes = b""
    for dbn, dct in dbn_to_dict.items():
        start, n = dbn[:2], dbn[2:]
        assert start == 'db', "Database numbers should take the form db0"
        n = int(n)
        if dct:
            data_bytes += convert_db(n, dct)

    finalized = wrap_start_end(data_bytes, redis_version=redis_version)

    bytesio.write(finalized)


def convert_db(db, dct):
    dbn = const.RDB_OPCODE_SELECTDB + bytes([db])
    fragment = convert_fragment(dct)
    return dbn + fragment


def convert_fragment(dct):
    data_bytes = b""

    for key, value in dct.items():

        bytes_key = convert_string(key)

        # Select data type
        if isinstance(value, bytes):
            typecode = const.RDB_TYPE_STRING
            bytes_value = convert_string(value)
        elif isinstance(value, set):
            typecode = const.RDB_TYPE_SET
            bytes_value = convert_list(value)
        elif isinstance(value, list) or isinstance(value, tuple):
            typecode = const.RDB_TYPE_LIST
            bytes_value = convert_list(value)
        elif isinstance(value, dict):
            typecode = const.RDB_TYPE_HASH
            bytes_value = convert_hash(value)
        else:
            raise ValueError("Invalid value in dict {}".format(value))

        data_bytes += typecode + bytes_key + bytes_value

    return data_bytes


def convert_string(string):
    assert isinstance(string, bytes),\
        "Use Python bytes objects to represent strings"
    length = encode_length(len(string))
    return length + string


def encode_length(length):
    if length <= 63:
        return length.to_bytes(1, byteorder='big')
    elif length <= 16383:
        return bytes([64 + length // 256, length % 256])
    else:
        return b'\x80' + length.to_bytes(4, byteorder='big')


def convert_list(lst):
    length = encode_length(len(lst))
    return length + b''.join([convert_string(s) for s in lst])


def convert_hash(hash):
    length = encode_length(len(hash))
    return length + b''.join(
        [convert_string(k)+convert_string(v) for k, v in hash.items()])


def wrap_start_end(data_bytes, redis_version=7):
    # Add preamble
    version = format(redis_version, '04d').encode('ascii')
    start = b'REDIS' + version

    end = const.RDB_OPCODE_EOF

    data = start + data_bytes + end

    checksum = crc64(data).to_bytes(8, byteorder='little')

    data += checksum

    return data

