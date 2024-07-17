#!/usr/bin/env python3
"""
12-log_stats.py
Script to provide statistics about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def count_logs(mongo_collection):
    """
    Count the total number of logs in the MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection object.

    Returns:
        int: Number of logs in the collection.
    """
    return mongo_collection.count_documents({})


def count_methods(mongo_collection):
    """
    Count the number of logs for each HTTP method: GET, POST, PUT, PATCH, DELETE.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection object.

    Returns:
        dict: Dictionary with counts for each method.
    """
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        method_counts[method] = mongo_collection.count_documents({"method": method})
    return method_counts


def count_status_check(mongo_collection):
    """
    Count the number of logs where method=GET and path=/status.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection object.

    Returns:
        int: Number of logs with method=GET and path=/status.
    """
    return mongo_collection.count_documents({"method": "GET", "path": "/status"})


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    total_logs = count_logs(nginx_collection)
    print("{} logs".format(total_logs))

    print("Methods:")
    methods_count = count_methods(nginx_collection)
    for method, count in methods_count.items():
        print("\tmethod {}: {}".format(method, count))

    status_check_count = count_status_check(nginx_collection)
    print("{} status check".format(status_check_count))
