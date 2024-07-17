#!/usr/bin/env python3
"""
102-log_stats
Script to provide statistics about Nginx logs stored in MongoDB,
including total logs, HTTP methods, and top IPs.
"""

from pymongo import MongoClient


def print_logs_stats(mongo_collection):
    """
    Print statistics about Nginx logs stored in MongoDB.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection object.
    """
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"    method {method}: {count}")

    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = list(mongo_collection.aggregate(pipeline))
    for ip in top_ips:
        print(f"    {ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    print_logs_stats(logs_collection)

