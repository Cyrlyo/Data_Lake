try:
    from mongoDB.utils_mongo import connectToMongo, strToDouble, doubleToInt, deleteEmptyString, countEmptyString, strToInt, strToBool, strToDate
except:
    from utils_mongo import connectToMongo, strToDouble, doubleToInt, deleteEmptyString, countEmptyString, strToInt, strToBool, strToDate
    
client, db = connectToMongo("localhost", 27017, "instagram")
posts = db["posts_reduced"]
locations = db["locations"]
profiles = db["profiles"]

# TODO: delete empty id string 
# convert str to int / double
# make location_id & profile_id as _id
# merge collections

#TODO: make function for each collections
if False:
    strToDouble(posts, "location_id")
    doubleToInt(posts, "location_id")
    strToDouble(posts, "profile_id")
    doubleToInt(posts, "profile_id")
    strToInt(posts, "post_type")
    strToDouble(posts, "numbr_likes")
    doubleToInt(posts, "numbr_likes")
    strToDouble(posts, "number_comments")
    doubleToInt(posts, "number_comments")
    strToDate(posts, "cts")

if False:
    countEmptyString(posts, "profile_id")
    deleteEmptyString(posts, "profile_id")
    
    strToInt(profiles, "profile_id")
    countEmptyString(profiles, "profile_id")
    deleteEmptyString(profiles, "profile_id")

    strToBool(profiles, "is_business_account")
    strToInt(profiles, "following")
    strToInt(profiles, "followers")
    strToInt(profiles, "n_posts")
    strToDate(profiles, "cts")

if False:
    strToInt(locations, "id")
    strToBool(locations, "aj_exact_city_match")
    strToBool(locations, "aj_exact_country_match")
    strToDouble(locations, "lat")
    strToDouble(locations, "lng")
    strToDate(locations, "cts")


# countEmptyString(profiles, "is_business_account")
# countEmptyString(profiles, "following")
# countEmptyString(profiles, "followers")
# countEmptyString(profiles, "n_posts")