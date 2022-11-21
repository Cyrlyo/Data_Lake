try:
    from mongoDB.utils_mongo import connectToMongo, strToDouble, doubleToInt, deleteEmptyString, countEmptyString, strToInt, strToBool
except:
    from utils_mongo import connectToMongo, strToDouble, doubleToInt, deleteEmptyString, countEmptyString, strToInt, strToBool
    
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
    deleteEmptyString(posts, "profile_id")
    
    strToInt(profiles, "profile_id")
    countEmptyString(profiles, "profile_id")
    deleteEmptyString(profiles, "profile_id")

strToBool(profiles, "is_business_account")

# countEmptyString(profiles, "is_business_account")
# countEmptyString(profiles, "following")
# countEmptyString(profiles, "followers")
# countEmptyString(profiles, "n_posts")