#!/usr/bin/env python3
"""
This module provides a function to fetch and cache web pages.
"""

import requests
import redis
from typing import Callable


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a function is called."""
    def wrapper(url: str) -> str:
        """Increment the count for each call."""
        cache = redis.Redis()
        cache_key_count = f"count:{url}"
        access_count = cache.incr(cache_key_count)
        print(f"URL {url} has been accessed {access_count} times.")
        return method(url)

    return wrapper


def cache_result(method: Callable) -> Callable:
    """Decorator to cache the result of a function in Redis."""
    def wrapper(url: str) -> str:
        """Fetches and caches the content of a web page."""
        cache = redis.Redis()
        cache_key_content = f"content:{url}"

        # Attempt to retrieve the cached content
        cached_content = cache.get(cache_key_content)
        if cached_content:
            print(f"Cache hit for {url}.")
            return cached_content.decode('utf-8')

        # Fetch the content and cache it with an expiration time of 10 seconds
        print(f"Cache miss for {url}. Fetching content.")
        response = method(url)
        cache.setex(cache_key_content, 10, response)
        return response

    return wrapper


@count_calls
@cache_result
def get_page(url: str) -> str:
    """Retrieve the HTML content of a URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text


if __name__ == "__main__":
    # Example usage
    test_url = (
        "http://slowwly.robertomurray.co.uk/delay/3000/url/"
        "https://example.com"
    )
    print(get_page(test_url))
    print(get_page(test_url))  # Should use cached version if within 10 seconds
