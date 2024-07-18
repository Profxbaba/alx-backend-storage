#!/usr/bin/env python3
"""This module provides a function to fetch and cache web pages."""

import requests
import redis
from typing import Callable


def cache_result(method: Callable) -> Callable:
    """Decorator to cache the result of a function in Redis."""
    def wrapper(url: str) -> str:
        """Fetches and caches the content of a web page."""
        cache = redis.Redis()
        cache_key = f"count:{url}"

        # Increment the access count for the URL
        cache.incr(cache_key)

        # Attempt to retrieve the cached content
        cached_content = cache.get(url)
        if cached_content:
            return cached_content.decode('utf-8')

        # Fetch the content and cache it with an expiration time of 10 seconds
        response = method(url)
        cache.setex(url, 10, response)
        return response
    return wrapper


@cache_result
def get_page(url: str) -> str:
    """Retrieve the HTML content of a URL."""
    response = requests.get(url)
    return response.text
