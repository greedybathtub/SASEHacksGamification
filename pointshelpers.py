import os
import addMongo

def get_points(username):
    user_doc = addMongo.users_col.find_one({"_id": username})
    if not user_doc or "pointsEarned" not in user_doc:
        return 0
    return user_doc["pointsEarned"]

def add_points(username, amount):
    result = addMongo.users_col.find_one_and_update(
        {"_id": username},
        {"$inc": {"pointsEarned": amount}},
        upsert=True,
        return_document=True
    )
    return result.get("pointsEarned", amount)

def get_hours(username):
    user_doc = addMongo.users_col.find_one({"_id": username})
    if not user_doc or "hoursLogged" not in user_doc:
        return 0
    return user_doc["hoursLogged"]

def add_hours(username, hours):
    points_to_add = hours * 5
    result = addMongo.users_col.find_one_and_update(
        {"_id": username},
        {"$inc": {"hoursLogged": hours, "pointsEarned": points_to_add}},
        upsert=True,
        return_document=True
    )
    return result.get("hoursLogged", 0), result.get("pointsEarned", 0)