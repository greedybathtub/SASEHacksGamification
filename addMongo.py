#Database connection and collection setup for Paws and Pages application
from pymongo import MongoClient

uri = "mongodb+srv://graeflaherty_db_user:oSnhJJzDbr6P6mDh@pawsandpages.1vd632v.mongodb.net/?appName=PawsandPages"

client = MongoClient(uri)
db = client["PawsandPages"]
users_col = db["UserInfo"]
messages_col = db["Messages"]
login_col = db["LoginData"]