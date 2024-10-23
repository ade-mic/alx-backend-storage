#!/usr/bin/env python3
"""
    Aggregation pipeline to calculate
    the average score and sort by it
"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Aggregation pipeline to calculate
    the average score and sort by it
    """
    pipeline = [
        {
            '$project': {
                'name': 1,
                'averageScore': {'$avg': '$topics.score'}
            }
        },
        {
            '$sort': {'averageScore': -1}
        }
    ]

    # Execute the aggregation pipeline
    return list(mongo_collection.aggregate(pipeline))
