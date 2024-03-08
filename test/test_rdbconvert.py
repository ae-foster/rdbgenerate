from __future__ import annotations

import io
from typing import TYPE_CHECKING

import pytest

from rdbgenerate import rdb_generate_io, RDBWriter

if TYPE_CHECKING:
    from rdbgenerate.rdbgen import REDIS_DB_TYPE

TEST_DATA = [
    (
        {},
        b"REDIS0007\xff\xb5\x6c\xfe\x83\xa7\x43\x1b\xdf",
    ),
    (
        {b"a": b"0"},
        b"REDIS0007\xfe\x00\x00\x01a\x010\xff\x08\x64\x37\x55\xe6\xfa\xc4\x4d",
    ),
    (
        {
            b"a": {
                b"0",
            }
        },
        b"REDIS0007\xfe\x00\x02\x01a\x01\x010\xff\x30\xeb\x26\xab\xeb\x94\xd7\xf3",
    ),
    (
        {
            b"a": [
                b"0",
            ]
        },
        b"REDIS0007\xfe\x00\x01\x01a\x01\x010\xff\x26\xdb\x21\x8e\xc0\x72\x2c\x54",
    ),
    (
        {b"a": {b"0": b"z"}},
        b"REDIS0007\xfe\x00\x04\x01a\x01\x010\x01z\xff\xb6\x76\xe4\x10\xed\x97\xce\xdc",
    ),
]


@pytest.mark.parametrize(
    "dct,binary",
    TEST_DATA
)
def test_rdbgenerate_io(
    dct: REDIS_DB_TYPE,
    binary: bytes,
) -> None:
    bytesio = io.BytesIO()
    rdb_generate_io(
        bytesio,
        db0=dct,
    )
    assert bytesio.getvalue() == binary


@pytest.mark.parametrize(
    "dct,binary",
    TEST_DATA
)
def test_rdbgenerate_stream(
    dct: REDIS_DB_TYPE,
    binary: bytes,
) -> None:
    bytesio = io.BytesIO()
    with RDBWriter(bytesio) as writer:
        if dct:
            writer.write_db(0)
            for key, value in dct.items():
                writer.write_fragment(key, value)
    assert bytesio.getvalue() == binary
