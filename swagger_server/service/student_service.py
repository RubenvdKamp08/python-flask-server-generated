import os
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient(os.environ['MONGO_URI'])
db = client.local
collection = db.students

id = db.info.find_one()
if not id:
    db.info.insert_one({ 'id_counter': 0 })

def get_id():
  id = db.info.find_one()['id_counter'] + 1
  db.info.update_many({}, { '$set': { 'id_counter': id } })
  return id

def add(student=None):
    res = collection.find_one({ 'first_name': student.first_name, 'last_name': student.last_name })
    if res:
        return 'already exists', 409

    student.student_id = get_id()
    student_dict = student.to_dict()
    collection.insert_one(student_dict)

    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = collection.find_one({'student_id': student_id})
    if not student:
        return 'not found', 404
    del student['_id']
    return student


def delete(student_id=None):
    _student = collection.find_one({'student_id': student_id})
    if not _student:
        return 'not found', 404
    collection.delete_one(({'student_id': student_id}))
    return student_id