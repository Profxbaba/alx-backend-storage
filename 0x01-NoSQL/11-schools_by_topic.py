#!/usr/bin/env python3
"""
11-schools_by_topic.py
Module to retrieve schools from MongoDB collection based on a specific topic using PyMongo.
"""

from pymongo.collection import Collection
from pymongo import MongoClient


def schools_by_topic(mongo_collection: Collection, topic: str):
    """
    Retrieves a list of schools from MongoDB collection based on a specific topic.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection object.
        topic (str): The topic to search for.

    Returns:
        list: List of school documents that match the topic.
    """
    schools = mongo_collection.find({"topics": topic})
    return list(schools)


if __name__ == "__main__":
    # Example usage
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.my_db
    school_collection = db.school
    
    # Sample data to insert
    j_schools = [
        {'name': "Holberton school", 'topics': ["Algo", "C", "Python", "React"]},
        {'name': "UCSF", 'topics': ["Algo", 
