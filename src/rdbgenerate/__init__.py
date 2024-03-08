from __future__ import annotations

from .rdbgen import rdb_generate, rdb_generate_io, RDBWriter

rdbgenerate = rdb_generate

__all__ = [
    "rdbgenerate",
    "rdb_generate",
    "rdb_generate_io",
    "RDBWriter",
]
