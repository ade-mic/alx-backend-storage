#!/usr/bin/env python3
"""
Module for a simple Redis-based cache system.

This module provides a Cache class that allows for storing data
in a Redis database with randomly generated keys.
"""
import redis
import uuid
from typing import Union


class Cache:
    """
    A Redis-based cache class that stores data using randomly generated keys
    
    Attributes:
        _redis (redis.Redis): A private Redis instance.
    """


    def __init__(self):
        """
        Initialize the Cache instance.

        This constructor initializes a Redis client and flushes all existing data
        from the Redis database to ensure a clean start
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis using a randomly generated key.
        
        Args:
            data (Union[str, bytes, int, float]): The data to be storedin Redis.

        Returns:
            str: The randomly generated key used the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
