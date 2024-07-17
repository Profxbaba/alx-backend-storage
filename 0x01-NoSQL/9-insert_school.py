#!/usr/bin/env python3
"""
9-insert_school.py
Module to insert a new document into a MongoDB collection using PyMongo.
"""

from pymongo.collection import Collection
from pymongo import MongoClient


def insert_school(mongo_collection: Collection, **kwargs) -> str:
    """
    Insert a new document into the MongoDB collection based on kwargs.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection object.
        **kwargs: Keyword arguments representing the fields and values for the new document.

    Returns:
        str: The new _id of the inserted document.
    """
    # Insert the document into the collection
    insert_result = mongo_collection.insert_one(kwargs)
    
    # Return the _id of the newly inserted document
    return str(insert_result.inserted_id)


if __name__ == "__main__":
    # Example usage
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.my_db
    school_collection = db.school
    
    # Insert a new
