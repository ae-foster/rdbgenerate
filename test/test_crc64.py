from __future__ import annotations

from rdbgenerate.crc64 import crc64


def test_crc64() -> None:
    input = b"123456789"
    output = crc64(input)
    assert output == 0xE9C6D914C4B8D9CA


if __name__ == "__main__":
    test_crc64()
