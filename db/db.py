from pymongo import MongoClient
from bson import  ObjectId

db_client = MongoClient("mongodb+srv://Maxfree:juegoroblox123@learning.xzyzvfd.mongodb.net/?retryWrites=true&w=majority")

database_list = db_client.todolist.list
database_user = db_client.todolist.users
