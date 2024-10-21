#!/usr/bin/env python3
"""
module that inserts a new document in a collection based on kwargs
Prototype: def insert_school(mongo_collection, **kwargs):
"""


def insert_school(mongo_collection, **kwargs):
    """
    inserts a new document in a collection based on kwargs:
    Args:
        mongo_collection(pymongo collection object)
        kwargs
    Return:
        return new _id
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id


if __name__ == "__main__":
    insert_school()
