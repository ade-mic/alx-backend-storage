#!/usr/bin/env python3
"""
Module for a simple Redis-based cache system.

This module provides a Cache class that allows for storing data
in a Redis database with randomly generated keys.
"""
from typing import Union, Optional, Callable
from functools import wraps
import uuid
import redis


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.

    Args:
        method (Callable): The method to be wrapped and counted.

    Returns:
        Callable: The wrapped method with counting functionality.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapped function that increments the call count in Redis.

        Args:
            self: The instance of the class (gives access to Redis).
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper

def replay(method: Callable) -> Callable:
    """
    function to display the history of calls
      of a particular function.
    """
    key = method.__qualname__
    redis_instance = method.__self__.redis

    call_count = int(redis_instance.get(key) or 0)
    print(f"{key} was called {call_count} times:")

    inputs = redis_instance.lrange(f"{key}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{key}:outputs", 0, -1)

    for input_args, output in zip(inputs, outputs):
        print(f"{key}(*{input_args.decode('utf-8')}) -> {output.decode('utf-8')}")

def call_history(method: Callable) -> Callable:
    """
    Decorator that store the history od inputs and outputs
    for a particualr function
    Args:
        method (Callable): The method to be wrapped and
                            add store its input and outputs.
    Returns:
        Callable: The wrapped method with history functionality.
    """

    @wraps(method)
    def wrapper(self, *args):
        """
        Wrapped function that stores the history in Redis.

            Returns:
        Callable: The wrapped method with history functionality.
        """
        output = method(self, *args)
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        self._redis.rpush(f"{method.__qualname__}:outputs", output)
        return output
    return wrapper


class Cache:
    """
    A Redis-based cache class that stores data using randomly generated keys
    Attributes:
        _redis (redis.Redis): A private Redis instance.
    """

    def __init__(self):
        """
        Initialize the Cache instance.

        This constructor initializes a Redis client and flushes
        all existing data
        from the Redis database to ensure a clean start
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis using a randomly generated key.
        Args:
            data (Union[str, bytes, int, float]):
            The data to be storedin Redis.

        Returns:
            str: The randomly generated key used the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[
                                    Callable[[bytes],
                                             Union[
                                                str, bytes, int, float
                                        ]]] = None) -> Union[
                                            str, bytes, int, float, None]:
        """
        Retrieve data from Redis by key, optionally applying
         a conversion function.

        Args:
            key (str): The key to retrieve the data from Redis.
            fn (Optional[Callable]): A function to apply
            for converting the retrieved data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved
            and optionally converted data.
            Returns None if the key does not exist.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis by key.

        Args:
            key (str): The key to retrieve the data from Redis.

        Returns:
            Optional[str]: The retrieved string,
             or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis by key.

        Args:
            key (str): The key to retrieve the data from Redis.

        Returns:
            Optional[int]: The retrieved integer,
             or None if the key does not exist.
        """
        return self.get(key, fn=int)
