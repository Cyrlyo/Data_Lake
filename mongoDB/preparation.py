try:
    from mongoDB.utils_mongo import connectToMongo, strToDouble, doubleToInt, deleteEmptyString,\
        countEmptyString, strToInt, strToBool, strToDate,\
        outCollections, deleteDuplicates, checkExistingCollection, createIndex, changeName, deleteStringType
except:
    from utils_mongo import connectToMongo, strToDouble, doubleToInt, deleteEmptyString,\
        countEmptyString, strToInt, strToBool, strToDate,\
        outCollections, deleteDuplicates, checkExistingCollection, createIndex, changeName, deleteStringType


def postsPreparation(posts, quick_prep:bool):
    """
    The function prepares the data in the `posts` collection by applying several data cleaning and type conversion steps.

    Parameters:
        posts: a collection (list, DataFrame, etc) of posts
        quick_prep (bool): A flag that indicates whether to perform a quick preparation (True) or a full preparation (False)
    """
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
        changeName(profiles, "profile_id", "id")

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

    deleteDuplicates(profiles, "id")
    deleteDuplicates(locations, "id")


def dataPreparation(host: str, port: int, database_name: str, collection_name: str,\
    quick_prep: bool, only_merge: bool, enable_merge: bool, sample: int):
    """
    The function connects to a MongoDB server and performs data preparation steps. 

    Parameters:
        host (str): the hostname or IP address of the MongoDB server
        port (int): the port number of the MongoDB server
        database_name (str): the name of the MongoDB database
        collection_name (str): the name of the collection that the final data should be stored in
        quick_prep (bool): flag that indicates whether to perform a quick data preparation or not
        only_merge (bool): flag that indicates whether to only perform merge operation or not
        enable_merge (bool): flag that indicates whether to perform merge operation or not
        sample (int): the size of the sample that should be used in the merge operation
    """
    client, db = connectToMongo(host, port, database_name)
    posts = db["posts_reduced"]
    locations = db["locations"]
    profiles = db["profiles"]
    
    if only_merge:
        changeDataType(posts, profiles, locations, quick_prep)
        deleteDuplicates(profiles, "id")
        deleteDuplicates(locations, "id")
        # createIndex(profiles, "id")
        # createIndex(locations, "id")
    
    if enable_merge:
        print("\nMerging... Please Wait")
        checkExistingCollection(db, "posts_details")
        # mergeColl(posts, "profiles", "locations", collection_name, "profile_id", "id", "profile", "location_id", "id", "location", sample)
        outCollections(posts, "profiles", "locations", collection_name, "profile_id", "id", "profile", "location_id", "id", "location", sample)