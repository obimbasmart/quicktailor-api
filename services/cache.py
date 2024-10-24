#!/usr/bin/env python3

"""Redis cache implementtion"""

import redis
from typing import Union, Callable, Any


class Cache:

    def __init__(self) -> None:
        self._redis = redis.Redis(host='127.0.0.1', port=6379)
        self._redis.flushdb()

    def store(self, key: str, data: Union[str, bytes, int, float], expires: int = 3600) -> str:
        self._redis.set(key, data, ex=expires)
        return key

    def get(self, key: str,
            fn: Union[Callable[[bytes], Any], None] = None) -> Any:
        data: bytes = self._redis.get(key)
        if data and fn is not None:
            return fn(data)
        return data

    def get_str(self, data: bytes) -> str:
        """convert to str"""
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """convert to integer"""
        return int(data)


cache = Cache()