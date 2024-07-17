#!/usr/bin/env python3
"""
This module provides a function to retrieve and cache
the HTML content of a URL using Redis.
"""

import redis
import requests
from functools import wraps
from typing import Callable


def cache_with_expiration(expiration: int) -> Callable:
    """
    Decorator to cache the result of a function with an expiration time.

    Args:
        expiration (int): The expiration time in seconds.

    Returns:
        Callable: The decorated function with caching.
    """
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str) -> str:
            """
            Wrapper function to cache the HTML content of a URL.

            Args:
                url (str): The URL to retrieve the content.

            Returns:
                str: The HTML content of the URL.
            """
            cache_key = f"cached:{url}"
            count_key = f"count:{url}"

            try:
                # Increment the access count for the URL
                redis_client.incr(count_key)

                # Check if the content is already cached
                cached_content = redis_client.get(cache_key)
                if cached_content:
                    return cached_content.decode('utf-8')

                # Retrieve and cache the content if not already cached
                content = method(url)
                redis_client.setex(cache_key, expiration, content)

                return content

            except (requests.RequestException, redis.RedisError) as e:
                print(f"Error accessing URL or Redis: {e}")
                return ""

        return wrapper

    return decorator


@cache_with_expiration(expiration=10)
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL.

    Args:
        url (str): The URL to retrieve the content.

    Returns:
        str: The HTML content of the URL.
    """
    try:
        response = requests.get(url)
        return response.text
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        return ""


# Initialize a Redis client
redis_client = redis.Redis()

if __name__ == "__main__":
    # Example usage
    url = ("http://slowwly.robertomurray.co.uk/delay/3000/url/"
           "http://www.example.com")
    print(get_page(url))
    print(redis_client.get(f"count:{url}").decode('utf-8'))
