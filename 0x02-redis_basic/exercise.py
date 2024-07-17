#!/usr/bin/env python3
"""
This module provides a Cache class for storing and retrieving data
in a Redis database with method call history tracking.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function with input/output history tracking.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store inputs and outputs in Redis.

        Args:
            self: The instance of the class.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            The result of the original function call.
        """
        # Create keys for storing inputs and outputs
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input arguments as a string
        self._redis.rpush(input_key, str(args))

        # Execute the original function
        result = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method with call counting.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to increment the call count and call the method.

        Args:
            self: The instance of the class.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The result of the original method call.
        """
        # Increment the call count in Redis using the method's qualified name
        self._redis.incr(method.__qualname__)
        # Call the original method and return its result
        return method(self, *args, **kwargs)

    return wrapper


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

    @call_history
    @count_calls
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


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.

    Args:
        method (Callable): The function whose call history is to be displayed.
    """
    # Create keys for inputs and outputs
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    # Retrieve the list of inputs and outputs from Redis
    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    # Display the history of calls
    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{inp.decode('utf-8')}) -> "
              f"{out.decode('utf-8')}")


if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store("foo")
    print(s1)
    s2 = cache.store("bar")
    print(s2)
    s3 = cache.store(42)
    print(s3)

    replay(cache.store)
