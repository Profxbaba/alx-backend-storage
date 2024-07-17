#!/usr/bin/env python3
"""
101-students
Script to retrieve all students sorted by average score from a MongoDB collection.
"""

from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Retrieve all students sorted by average score from the MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection object.

    Returns:
        list: List of dictionaries, each containing '_id', 'name', and 'averageScore'.
    """
    pipeline = [
        {"$project": {
            "name": 1,
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ]
    students = list(mongo_collection.aggregate(pipeline))
    for student in students:
        student['_id'] = str(student['_id'])  # Convert ObjectId to string
    return students


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students

    # Example data insertion
    j_students = [
        {'name': "John", 'topics': [{'title': "Algo", 'score': 10.3}, {'title': "C", 'score': 6.2}, {'title': "Python", 'score': 12.1}]},
        {'name': "Bob", 'topics': [{'title': "Algo", 'score': 5.4}, {'title': "C", 'score': 4.9}, {'title': "Python", 'score': 7.9}]},
        {'name': "Sonia", 'topics': [{'title': "Algo", 'score': 14.8}, {'title': "C", 'score': 8.8}, {'title': "Python", 'score': 15.7}]},
        {'name': "Amy", 'topics': [{'title': "Algo", 'score': 9.1}, {'title': "C", 'score': 14.2}, {'title': "Python", 'score': 4.8}]},
        {'name': "Julia", 'topics': [{'title': "Algo", 'score': 10.5}, {'title': "C", 'score': 10.2}, {'title': "Python", 'score': 10.1}]}
    ]
    for j_student in j_students:
        insert_school(students_collection, **j_student)

    # Displaying all students (just for verification)
    students = list_all(students_collection)
    for student in students:
        print("[{}] {} - {}".format(student.get('_id'), student.get('name'), student.get('topics')))

    # Retrieving and displaying top students
    top_students_list = top_students(students_collection)
    for student in top_students_list:
        print("[{}] {} => {}".format(student.get('_id'), student.get('name'), student.get('averageScore')))

