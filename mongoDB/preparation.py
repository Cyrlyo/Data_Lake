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
        countEmptyString(posts, "profile_id")
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
    
    

def profilesPreparation(profiles):
    
    str_to_int_list = ["profile_id", "following", "followers", "n_posts"]
    
    for variable in str_to_int_list:
        strToInt(profiles, str(variable))
        countEmptyString(profiles, str(variable))
        deleteEmptyString(profiles, str(variable))

    strToBool(profiles, "is_business_account")
    countEmptyString(profiles, "is_business_account")
    deleteEmptyString(profiles, "is_business_account")
    strToDate(profiles, "cts")
    countEmptyString(profiles, "cts")
    deleteEmptyString(profiles, "cts")
    

    # strToInt(profiles, "profile_id")
    # countEmptyString(profiles, "profile_id")
    # deleteEmptyString(profiles, "profile_id")

    # strToInt(profiles, "following")
    # strToInt(profiles, "followers")
    # strToInt(profiles, "n_posts")

    

def locationsPreparation(locations):

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