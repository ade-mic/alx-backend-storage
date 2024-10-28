#!/usr/bin/env python3
"""
 implement a get_page function
"""
import requests
import redis
from typing import Callable
from functools import wraps
import hashlib
# Initialize Redis client
cache = redis.Redis()


def cache_page(func: int = 10) -> Callable:
    """
    Decorator to cache the HTML content of a URL with an expiration time.
    Tracks how many times each URL is accessed.
    """
    @wraps(func)
    def wrapper(url):
        # Generate a unique key for the URL content
        url_hash = hashlib.sha256(url.encode()).hexdigest()
        cache_key = f"page:{url_hash}"
        count_key = f"count:{url_hash}"

        # Check if the page content is already cached
        cached_page = cache.get(cache_key)
        if cached_page:
            # Increment the access count for the URL in Redis
            cache.incr(count_key)
            return cached_page.decode('utf-8')

        # If not cached, call the original function to get the page
        page_content = func(url)

        # Store the page content in Redis with a 10-second expiration
        cache.setex(cache_key, 10, page_content)
        # Initialize access count to 1
        cache.set(count_key, 1)

        return page_content
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Fetch HTML content of a URL, with caching and access count tracking.

    Args:
        url (str): The URL to retrieve content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text
