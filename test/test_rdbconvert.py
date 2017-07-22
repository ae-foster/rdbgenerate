import pytest
from rdbgenerate.rdbgen import rdb_generate_io
import io

@pytest.mark.parametrize(
    "dct,binary",[
    ({}, b'REDIS0007\xff\xb5l\xfe\x83\xa7C\x1b\xdf'),
    ({b"a": b"0"}, b'REDIS0007\xfe\x00\x00\x01a\x010\xff\x08d7U\xe6\xfa\xc4M'),
    ({b"a": {b"0", }}, b'REDIS0007\xfe\x00\x02\x01a\x01\x010\xff0\xeb&\xab\xeb\x94\xd7\xf3'),
    ({b"a": [b"0", ]}, b'REDIS0007\xfe\x00\x01\x01a\x01\x010\xff&\xdb!\x8e\xc0r,T'),
    ({b"a": {b"0": b"z"}}, b'REDIS0007\xfe\x00\x04\x01a\x01\x010\x01z\xff\xb6v\xe4\x10\xed\x97\xce\xdc')]
)
def test_rdbgenerate_io(dct, binary):
    bytesio = io.BytesIO()
    rdb_generate_io(bytesio, db0=dct)
    value = bytesio.getvalue()
    print(value)
    assert value == binary
