from pymongo import MongoClient

# Replace with your connection string
uri = "mongodb+srv://graeflaherty_db_user:oSnhJJzDbr6P6mDh@pawsandpages.1vd632v.mongodb.net/?appName=PawsandPages"

client = MongoClient(uri)
db = client["PawsandPages"]          # Database
users_col = db["users"]              # Users collection
messages_col = db["messages"]        # Messages collection