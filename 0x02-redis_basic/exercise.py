#!/usr/bin/env python3
"""This module provides a Cache class for storing data using Redis."""

from typing import Callable
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that increments call count."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Cache class for storing and retrieving data using Redis."""

    def __init__(self):
        """Initialize Redis client."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: bytes) -> None:
        """Store data in Redis."""
        self._redis.set(data, data)

    def get(self, key: str) -> bytes:
        """Retrieve data from Redis."""
        return self._redis.get(key)
