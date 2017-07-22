# These constants were taken from https://github.com/antirez/redis/blob/unstable/src/rdb.h
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

RDB_TYPE_STRING = b'\x00'
RDB_TYPE_LIST = b'\x01'
RDB_TYPE_SET = b'\x02'
RDB_TYPE_ZSET = b'\x03'
RDB_TYPE_HASH = b'\x04'
RDB_TYPE_ZSET_2 = b'\x05' # ZSET version 2 with doubles stored in binary.

RDB_TYPE_HASH_ZIPMAP = b'\x09'
RDB_TYPE_LIST_ZIPLIST = b'\x0a'
RDB_TYPE_SET_INTSET = b'\x0b'
RDB_TYPE_ZSET_ZIPLIST = b'\x0c'
RDB_TYPE_HASH_ZIPLIST= b'\x0d'
RDB_TYPE_LIST_QUICKLIST = b'\x0e'

RDB_OPCODE_EOF = b'\xff'
RDB_OPCODE_SELECTDB = b'\xfe'
