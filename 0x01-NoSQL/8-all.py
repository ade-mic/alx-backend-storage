#!/usr/bin/env python3
"""
This module  lists all documents in a collection in MongoDB.
"""


def list_all(mongo_collection):
    """
    lists all documents in a collection mongo_collection.
    Args:
        mongo_collection(pymongo collection object)
    Return:
        empty list if no document in the collection
    """
    doc = list(mongo_collection.find())
    return doc


if __name__ == "__main__":
    list_all()
