try:
    from mongoDB.utils_mongo import connectToMongo, strToDouble, doubleToInt
except:
    from utils_mongo import connectToMongo, strToDouble, doubleToInt
    
client, db = connectToMongo("localhost", 27017, "instagram")
posts = db["posts_reduced"]
locations = db["locations"]
profiles = db["profiles"]

# TODO: delete empty id string 
# convert str to int / double
# merge collections


if False:
    strToDouble(posts, "location_id")
    doubleToInt(posts, "location_id")
    strToDouble(posts, "profile_id")
    doubleToInt(posts, "profile_id")


def deleteEmptyString(collection, variable: str):
    
    collection.remove({variable: {"$type": "string", "$eq":""}})