# rdbgenerate
Utility for generating Redis dump (.rdb) files from Python native objects

## Installation
(TODO)
You can install this using `pip`?

## Version support
`rdbgenerate` is written for Python 3.

## Usage
Once installed, use `rdb_generate` to write `.rdb` files.


    >>> from rdbgenerate import rdb_generate
    >>> rdb_generate(
            'dump.rdb',
            db0={
                b"a": b"0",
                b"b": {b"1"},
                b"c": [b"1", b"2", b"3"],
                b"d": {b"x": b"y"}
            },
            db1={
                b"California": b"dreamin'"
            }
        )

### Encodings
This package supports strings that are Python `bytes` objects. It does *not* support regular Python strings.
Python strings can be converted to `bytes` via

    >>> s = "California"
    >>> b = s.encode('utf8')
    >>> print(b)
    b"California"
    
For more information on string encoding in Python 3, see https://docs.python.org/3/howto/unicode.html .