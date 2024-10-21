#!/usr/bin/env python3
"""
that changes all topics of a school document based on the name
Prototype: def update_topics(mongo_collection, name, topics):
"""


def update_topics(mongo_collection, name, topics):
    """
    changes all topics of a school document based on the name
    Args:
        mongo_collection(mongodb collection)
        name (string)
        topics (list of strings)
    """
    results = mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})


if __name__ == "__main__":
    update_topics()
