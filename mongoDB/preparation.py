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

def postsPreparation(posts):
    
    str_to_int_list = ["location_id", "profile_id", "number_comments", "numbr_likes"]
    
    for variable in str_to_int_list:
        
        strToDouble(posts, str(variable))
        doubleToInt(posts, str(variable))
        deleteEmptyString(posts, str(variable))
    
    strToInt(posts, "post_type")
    strToDate(posts, "cts")
    deleteEmptyString(posts, "post_type")
    deleteEmptyString(posts, "cts")
    
    # strToDouble(posts, "location_id")
    # doubleToInt(posts, "location_id")
    
    # strToDouble(posts, "profile_id")
    # doubleToInt(posts, "profile_id")

    # strToDouble(posts, "number_comments")
    # doubleToInt(posts, "number_comments")
    
    # strToDouble(posts, "numbr_likes")
    # doubleToInt(posts, "numbr_likes")
    
    

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