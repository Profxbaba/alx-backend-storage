#!/usr/bin/env python3
"""
10-update_topics.py
Module to update the topics of a school document in a MongoDB collection using PyMongo.
"""

from pymongo.collection import Collection
from pymongo import MongoClient


def update_topics(mongo_collection: Collection, name: str, topics: list):
    """
    Updates the topics of a school document based on its name.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection object.
        name (str): The name of the school to update.
        topics (list): The list of topics to set in the school document.
    """
    mongo_collection.update_one(
        {"name": name},
        {"$set": {"topics": topics}}
    )


if __name__ == "__main__":
    # Example usage
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.my_db
    school_collection = db.school
    
    update_topics(school_collection, "Holberton school", ["Sys admin", "AI", "Algorithm"])

    # Verify the update
    from pymongo.collection import Collection
    list_all = __import__('8-all').list_all
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'), school.get('name'), school.get('topics', "")))

    update_topics(school_collection, "Holberton school", ["iOS"])

    # Verify the update again
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'), school.get('name'), school.get('topics', "")))
