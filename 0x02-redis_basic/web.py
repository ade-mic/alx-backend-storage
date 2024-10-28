#!/usr/bin/env python3
"""Module implement web req"""
import requests
import redis
from functools import wraps
from typing import Callable

cache = redis.Redis()


def cache_with_count_and_expiry(expire_time: int = 10) -> Callable:
    """
    A decorator to cache the result of a function in Redis, track access count,
    and set an expiration time for the cached data.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Generate cache keys for count and HTML content
            count_key = f"count:{url}"
            content_key = f"content:{url}"

            # Increment access count for the URL
            cache.incr(count_key)

            # Check if the content is already cached
            cached_content = cache.get(content_key)
            if cached_content:
                return cached_content.decode('utf-8')

            # If not cached, fetch the content, cache it, and set expiration
            result = func(url)
            cache.setex(content_key, expire_time, result)
            return result
        return wrapper
    return decorator


@cache_with_count_and_expiry(expire_time=10)
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL, caching the
      result with a 10-second expiry.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
