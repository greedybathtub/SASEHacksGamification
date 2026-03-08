#Database connection and collection setup for Paws and Pages application
from pymongo import MongoClient

uri = MONGO_URI

client = MongoClient(uri)
db = client["PawsandPages"]
users_col = db["UserInfo"]
messages_col = db["Messages"]
login_col = db["LoginData"]