#!/usr/bin/env python3
"""
 implement a get_page function
"""
import requests
import redis
from typing import Callable
from functools import wraps

cache = TTLCache(maxsize=100, ttl=10)


def cache_decorator(func: Callable) -> Callable:
    """Decorator to cache function results and track access counts."""
    def wrapper(url: str) -> str:
        # Track access count
        if f"count:{url}" not in cache:
            cache[f"count:{url}"] = 0
        cache[f"count:{url}"] += 1

        # Use cachetools' cached decorator to cache the result
        return cached(cache)(func)(url)
    return wrapper


@cache_decorator
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and cache the result.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.text
