#Database connection and collection setup for Paws and Pages application
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGO_URI")

client = MongoClient(uri)
db = client["PawsandPages"]
users_col = db["UserInfo"]
messages_col = db["Messages"]
login_col = db["LoginData"]