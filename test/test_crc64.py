from rdbgenerate.crc64 import crc64

def test_crc64():
    input = b"123456789"
    output = crc64(input)
    assert output == 0xe9c6d914c4b8d9ca

if __name__ == '__main__':
    test_crc64()