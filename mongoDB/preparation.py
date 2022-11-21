try:
    from mongoDB.utils_mongo import connectToMongo, strToDouble, doubleToInt, deleteEmptyString, countEmptyString, strToInt, strToBool, strToDate
except:
    from utils_mongo import connectToMongo, strToDouble, doubleToInt, deleteEmptyString, countEmptyString, strToInt, strToBool, strToDate
    


# TODO: delete empty id string 
# convert str to int / double
# make location_id & profile_id as _id
# merge collections

def postsPreparation(posts):
    
    str_to_int_list = ["location_id", "profile_id", "number_comments", "numbr_likes"]
    
    for variable in str_to_int_list:
        
        strToDouble(posts, str(variable))
        doubleToInt(posts, str(variable))
        countEmptyString(posts, variable)
        deleteEmptyString(posts, str(variable))
    
    strToInt(posts, "post_type")
    strToDate(posts, "cts")
    deleteEmptyString(posts, "post_type")
    deleteEmptyString(posts, "cts")

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

def locationsPreparation(locations):

    strToInt(locations, "id")
    
    strToBool(locations, "aj_exact_city_match")
    strToBool(locations, "aj_exact_country_match")
    
    strToDouble(locations, "lat")
    strToDouble(locations, "lng")
    
    strToDate(locations, "cts")

def dataPreparation(host: str, port: int, database_name: str):
    
    client, db = connectToMongo(host, port, database_name)
    posts = db["posts_reduced"]
    locations = db["locations"]
    profiles = db["profiles"]
    
    print("\nprofiles preparation... Please wait")
    profilesPreparation(profiles)
    print("done")
    print("\nposts preparation... Please wait")
    postsPreparation(posts)
    print("done")
    print("\nlocations preparation... Please wait")
    locationsPreparation(locations)
    print("done")