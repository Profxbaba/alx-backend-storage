#!/usr/bin/env python3
"""
8-all.py
Module to list all documents in a MongoDB collection using PyMongo.
"""

from pymongo.collection import Collection
from pymongo import MongoClient


def list_all(mongo_collection: Collection) -> list:
    """
    Lists all documents in the given MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection object.

    Returns:
        list: A list of all documents in the collection. Returns an empty list if no documents are found.
    """
    cursor = mongo_collection.find({})  # Retrieve all documents

    # Convert cursor to list of documents
    documents = list(cursor)

    return documents


if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.my_db
    collection = db.school

    # Retrieve and print all documents in the collection
    schools = list_all(collection)
    for school in schools:
        print("[{}] {}".format(school.get('_id'), school.get('name')))
