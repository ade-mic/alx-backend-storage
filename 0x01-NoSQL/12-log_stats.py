#!/usr/bin/env python3
"""
a Python script that provides some stats about Nginx logs
stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
first line: x logs where x is the number of documents in this
collection
second line: Methods:
5 lines with the number of documents with
the method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
in this order (see example below - warning: it’s a tabulation
before each line)
one line with the number of documents with:
method=GET
path=/status
"""
from pymongo import MongoClient
if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    ngix_collection = client.logs.nginx
    print(f"{ngix_collection.count_documents({})} logs\nMethods: \n \t method GET: {ngix_collection.count_documents({'method': 'GET'})} \
            \n \t method POST: {ngix_collection.count_documents({'method': 'POST'})}\
            \n \t method PUT: {ngix_collection.count_documents({'method': 'PUT'})}\
            \n \t method PATCH: {ngix_collection.count_documents({'method': 'PATCH'})}\
            \n \t method DELETE: {ngix_collection.count_documents({'method': 'DELETE'})}\
            \n {ngix_collection.count_documents({'path': '/status'})} status check")
