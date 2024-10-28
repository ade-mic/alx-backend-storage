"""
 implement a get_page function
"""
import requests
import redis
from typing import Callable
from functools import wraps

# Initialize Redis client
cache = redis.Redis()


def cache_page(expire_time: int = 10) -> Callable:
    """
    Decorator to cache the HTML content of a URL with an expiration time.
    Tracks how many times each URL is accessed.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Track access count for the URL
            count_key = f"count:{url}"
            content_key = f"content:{url}"

            cache.incr(count_key)

            cached_content = cache.get(content_key)
            if cached_content:
                return cached_content.decode('utf-8')

            result = func(url)
            cache.setex(content_key, expire_time, result)
            return result
        return wrapper
    return decorator


@cache_page(expire_time=10)
def get_page(url: str) -> str:
    """
    Fetch HTML content of a URL, with caching and access count tracking.

    Args:
        url (str): The URL to retrieve content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
