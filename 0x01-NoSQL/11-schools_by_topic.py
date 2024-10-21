#!/usr/bin/env python3
"""
module returns the list of school having a specific topic:

Prototype: def schools_by_topic(mongo_collection, topic):
mongo_collection will be the pymongo collection object
topic (string) will be topic searched
"""


def schools_by_topic(mongo_collection, topic):
    """
    returns the list of school having a specific topic
    """

    results = mongo_collection.find({"topics": topic})
    return list(results)


if __name__ == "__main__":
    schools_by_topic()