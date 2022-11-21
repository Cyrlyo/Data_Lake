try:
    from mongoDB.utils_mongo import connectToMongo, strToDouble, doubleToInt, deleteEmptyString, countEmptyString
except:
    from utils_mongo import connectToMongo, strToDouble, doubleToInt, deleteEmptyString, countEmptyString
    
client, db = connectToMongo("localhost", 27017, "instagram")
posts = db["posts_reduced"]
locations = db["locations"]
profiles = db["profiles"]

# TODO: delete empty id string 
# convert str to int / double
# make location_id & profile_id as _id
# merge collections


if False:
    strToDouble(posts, "location_id")
    doubleToInt(posts, "location_id")
    strToDouble(posts, "profile_id")
    doubleToInt(posts, "profile_id")

countEmptyString(posts, "profile_id")
# deleteEmptyString(posts, "profile_id")