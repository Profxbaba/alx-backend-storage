#!/usr/bin/env python3

import requests
import redis
from functools import wraps
from typing import Callable, Any

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def cache_result(ttl: int = 10) -> Callable[[Callable[[str], str]], Callable[[str], str]]:
    """
    A decorator to cache the result of a function with a given TTL.

    Args:
        ttl (int): The time to live in seconds.

    Returns:
        A decorator function.
    """
    def decorator(func: Callable[[str], str]) -> Callable[[str], str]:
        """
        A decorator function to cache the result of a function.

        Args:
            func (Callable[[str], str]): The function to be decorated.

        Returns:
            A decorated function.
        """
        @wraps(func)
        def wrapper(url: str) -> str:
            """
            A wrapper function to cache the result of a function.

            Args:
                url (str): The URL to fetch.

            Returns:
                str: The HTML content of the URL.
            """
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"
            if redis_client.exists(cache_key):
                return redis_client.get(cache_key).decode('utf-8')
            else:
                result = func(url)
                redis_client.setex(cache_key, ttl, result)
                redis_client.incr(count_key)
                return result
        return wrapper
    return decorator


@cache_result(ttl=10)
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
