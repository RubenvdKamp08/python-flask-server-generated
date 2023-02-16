import os
from pymongo import MongoClient

client = MongoClient(os.environ['MONGO_URI'])
database = client.local
student_collection = database.students

# Get the current id counter, otherwise create a counter
id = database.info.find_one()
if not id:
    database.info.insert_one({ 'counter': 0 })

# Get the current id counter and increment this value to make sure this will be unique
def get_id():
  id = database.info.find_one()['counter'] + 1
  database.info.update_many({}, {'$set': {'counter': id}})
  return id

def add(student=None):
    res = student_collection.find_one({ 'first_name': student.first_name, 'last_name': student.last_name })
    if res:
        return 'already exists', 409

    # Add the id to the student_id
    student.student_id = get_id()
    # Create a dict and add this to the collection
    student_dict = student.to_dict()
    student_collection.insert_one(student_dict)

    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = student_collection.find_one({'student_id': student_id})
    if not student:
        return 'not found', 404
    # Delete the document id, because not valuable in response
    del student['_id']
    return student


def delete(student_id=None):
    student = student_collection.find_one({'student_id': student_id})
    if not student:
        return 'not found', 404
    student_collection.delete_one(({'student_id': student_id}))
    return student_id