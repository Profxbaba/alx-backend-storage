#!/usr/bin/env python3
"""
This module provides a Cache class for storing and retrieving data
in a Redis database.
"""

import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """
    Cache class for storing and retrieving data in Redis.
    """

    def __init__(self) -> None:
        """
        Initialize the Cache instance by connecting to Redis
        and flushing the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The randomly generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the provided key and an optional
        conversion function.

        Args:
            key (str): The key to retrieve the data.
            fn (Optional[Callable]): The function to convert the data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data,
            possibly converted using fn, or None if key does not exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string from Redis using the provided key.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Optional[str]: The retrieved string or None if key does not exist.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis using the provided key.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Optional[int]: The retrieved integer or None if key does not exist.
        """
        return self.get(key, lambda d: int(d))


if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
