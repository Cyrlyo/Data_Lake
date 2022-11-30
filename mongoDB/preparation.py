try:
    from mongoDB.utils_mongo import connectToMongo, strToDouble, doubleToInt, deleteEmptyString, countEmptyString, strToInt, strToBool, strToDate,\
        mergeColl, outCollections, deleteDuplicates, checkExistingCollection
except:
    from utils_mongo import connectToMongo, strToDouble, doubleToInt, deleteEmptyString, countEmptyString, strToInt, strToBool, strToDate,\
        mergeColl, outCollections, deleteDuplicates, checkExistingCollection
    


# TODO: delete empty id string 
# convert str to int / double
# make location_id & profile_id as _id
# merge collections
# TODO: make switch full preparation vs half prep

# TODO: add allowDiskUse = True in aggregate ! 
# It should reduce the time takes by query

def postsPreparation(posts, quick_prep:bool):
    #TODO: add $sample in the aggregation query to reduce number of posts! Only for the first and make a condition
    # to take only the good data type of the first data type changed
    # this should reduce time for each query !
    str_to_int_list = ["location_id", "profile_id", "number_comments", "numbr_likes"]
    
    for variable in str_to_int_list:
        
        deleteEmptyString(posts, str(variable))
        strToDouble(posts, str(variable))
        doubleToInt(posts, str(variable))
        countEmptyString(posts, variable)
    
    if quick_prep:
        deleteEmptyString(posts, "post_type")
        deleteEmptyString(posts, "cts")
        strToInt(posts, "post_type")
        strToDate(posts, "cts")

def profilesPreparation(profiles, quick_prep: bool):
    """Changing data type from str to int64, double or boolean.
    Every data type covert takes around 10 minutes.

    Args:
        profiles (MongoCollection): Mongo Collection
        quick_prep (bool): switch that convert data type only for
            necessary variables
    """
    
    str_to_int_list = ["profile_id", "following", "followers", "n_posts"]
    
    for variable in str_to_int_list:
        deleteEmptyString(profiles, str(variable))
        strToInt(profiles, str(variable))
        countEmptyString(profiles, str(variable))

    if quick_prep:
        deleteEmptyString(profiles, "is_business_account")
        strToBool(profiles, "is_business_account")
        countEmptyString(profiles, "is_business_account")
        deleteEmptyString(profiles, "cts")
        strToDate(profiles, "cts")
        countEmptyString(profiles, "cts")

def locationsPreparation(locations, quick_prep: bool):

    strToInt(locations, "id")
    
    if quick_prep:
        strToBool(locations, "aj_exact_city_match")
        strToBool(locations, "aj_exact_country_match")

        strToDouble(locations, "lat")
        strToDouble(locations, "lng")

        strToDate(locations, "cts")


def changeDataType(posts, profiles, locations, quick_prep: bool):
    
    print("\nprofiles preparation... Please wait")
    profilesPreparation(profiles, quick_prep)
    print("done")
    print("\nposts preparation... Please wait")
    postsPreparation(posts, quick_prep)
    print("done")
    print("\nlocations preparation... Please wait")
    locationsPreparation(locations, quick_prep)
    print("done")

    deleteDuplicates(profiles, "profile_id")
    deleteDuplicates(locations, "id")
    

def dataPreparation(host: str, port: int, database_name: str, collection_name: str,\
    quick_prep: bool, only_merge: bool, desac_merge: bool):
    """_summary_

    Args:
        host (str): _description_
        port (int): _description_
        database_name (str): _description_
        collection_name (str): _description_
        quick_prep (bool): _description_
        only_merge (bool): _description_
    """
    
    client, db = connectToMongo(host, port, database_name)
    posts = db["posts_reduced"]
    locations = db["locations"]
    profiles = db["profiles"]
    
    if only_merge:
        changeDataType(posts, profiles, locations, quick_prep)
    
    if desac_merge:
        print("Merging... Please Wait")
        # mergeColl(posts, "profiles", "locations", collection_name, "profile_id", "id", "profile", "location_id", "id", "location")
        checkExistingCollection(db, "posts_details")
        outCollections(posts, "profiles", "locations", collection_name, "profile_id", "id", "profile", "location_id", "id", "location")