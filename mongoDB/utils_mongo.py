import csv
import json
import os
from pathlib import Path
from pymongo import MongoClient
from pymongo.operations import IndexModel
from tqdm import tqdm
import pymongo

def csvToJson(csv_path_file: str, json_path_file: str):
    """_summary_

    Args:
        csv_path_file (str): _description_
        json_path_file (str): _description_
    """
    result, createPath = pathChecker(json_path_file)
    if not result:
        os.makedirs(createPath)
    
    json_array = []
    
    with open(csv_path_file, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter="\t")
        
        for row in csv_reader:
            json_array.append(row)
    print("Extracting json... please wait\nIt can take time.")

    with open(json_path_file, "w", encoding="utf-8") as json_file:
        json_string = json.dumps(json_array, ensure_ascii=False)
        json_file.write(json_string)
    
    print("Done")

def pathChecker(path: str) -> bool:
    """_summary_

    Args:
        path (str): _description_

    Returns:
        bool: _description_
    """
    
    result_dict = {True: "exists", False: "doesn't exist"}
    
    splited_path = Path(path).parts
    formated_path = os.path.join(*splited_path[: -1])
    result = os.path.exists(formated_path)
    print(f"\n'{formated_path}' {result_dict[result]}")
    
    return result, formated_path

def connectToMongo(host: str, port: int, database_name: str):
    """_summary_

    Args:
        host (str): _description_
        port (int): _description_

    Returns:
        MongoClient: _description_
    """
    
    client = MongoClient(host, port)
    db = client[database_name]
    
    return client, db

def mongoPythonLoad(data_path: str, collection):
    """
    USE ONLY IF NECESSARY! IT TAKES A LOT OF TIME! MORE THAN 30MIN FOR 
    ONLY ONE DOCUMENT!
    Need using conneToMongo before.
    
    Args:
        data_path (str): _description_
        collection (PyMongo Collection Object)! _description_
    """
    
    with open(data_path, encoding="utf-8") as file:
        file_data = json.load(file)
        
    for doc, tq in zip(file_data, tqdm(range(len(file_data)))):
        collection.insert_one(doc)

def mongoQueryLoad(database_name: str, collection_name: str, host: str, port: int, file_path: str):
    """
    NEED MONGOIMPORT INSTALLED ON YOUR DEVICE!
    If collections already exist they'll be droped and recreated.    
    Args:
        database_name (str): _description_
        host (str): by default localhost i.e. 127.0.0.1
        port (int): by default 27017
        file_path (str): _description_
    """
    
    os.system(f'mongoimport --host {host} -d {database_name} --port {port}\
        --collection {collection_name} --file {file_path} --jsonArray --drop')

def deleteDuplicates(collection, id_field: str):
    cursor = collection.aggregate(
    [
        {"$group": {"_id": "$%s"%id_field, "unique_ids": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
        {"$match": {"count": { "$gte": 2 }}}
    ], allowDiskUse=True)

    response = []
    for doc in cursor:
        del doc["unique_ids"][0]
        for id in doc["unique_ids"]:
            response.append(id)

    collection.delete_many({"_id": {"$in": response}})

def createIndex(collection, field_to_index: str):
    
    index = IndexModel([(field_to_index, pymongo.ASCENDING)], unique=True)
    collection.create_index([index])

def strToDouble(collection, variable: str):
    
    collection.update_many({variable: {"$type": "string", "$ne":""}}, [{"$set": {variable: {"$toDouble": "$%s"% variable}}}])

def strToInt(collection, variable: str):
    
    collection.update_many({variable: {"$type": "string", "$ne": ""}}, [{"$set": {variable: {"$convert": {"input": "$%s"% variable, "to": "long"}}}}])

def strToBool(collection, variable: str):
    
    collection.update_many({variable: {"$type": "string", "$ne": ""}}, [{"$set": {variable: {"$convert": {"input": "$%s"% variable, "to": "bool"}}}}])

def doubleToInt(collection, variable: str):
    
    collection.update_many({variable: {"$type": "double"}}, [{"$set": {variable: {"$convert": {"input": "$%s"% variable, "to": "long"}}}}])
    
def deleteEmptyString(collection, variable: str):
    
    collection.delete_many({variable: {"$type": "string", "$eq":""}})

def deleteStringType(collection, variable: str):
    
    collection.delete_many({variable: {"$type": "string"}})


def countEmptyString(collection, variable: str):
    
    results = collection.aggregate([{"$match": {variable: {"$eq": ""}}}, {"$group": {"_id": "null", "count": {"$sum": 1}}}])
    for result in results:
        print(f"Number of null string in '{variable}': {result[list(result.keys())[-1]]}")

def changeName(collection, old_name: str, new_name: str):
    collection.update_many({}, {"$rename": {str(old_name): str(new_name)}})

def strToDate(collection, variable: str):
    
    collection.update_many({variable: {"$type": "string", "$ne": ""}}, [{"$set": {variable: {"$convert": {"input": "$%s"% variable, "to": "date"}}}}])

def mergeColl(collection, profiles: str, locations: str, collection_name: str, localProfiles: str, foreignProfiles: str,
              newProfileName: str, localLocation: str, foreignLocation: str, newLocationName: str, sample: int):
    """
    The function performs an aggregate operation on the provided collection and exports the result to a new collection 
    with the specified name `collection_name`. The operation includes a sample of the collection with size `sample` documents 
    and join the collection with two other collections `profiles`, and `locations` based on the `localField` and `foreignField`
    and rename them with `newProfileName` and `newLocationName` respectively. The function also projects some fields and 
    hides some.

    Parameters:
        collection: a pymongo Collection object
        profiles (str): name of the collection that should be joined as profiles
        locations (str): name of the collection that should be joined as locations
        collection_name (str): the name of the new collection that should be created
        localProfiles (str): the field on the collection that is used as the join field with profiles collection
        foreignProfiles (str): the field on the profiles collection that is used as the join field
        newProfileName (str): the name of the array that contains the joined profile documents
        localLocation (str): the field on the collection that is used as the join field with locations collection
        foreignLocation (str): the field on the location collection that is used as the join field
        newLocationName (str): the name of the array that contains the joined location documents
        sample (int): the number of documents to be sampled
    """

    collection.aggregate([{"$sample": {"size":sample}},\
    {'$lookup': {'from': profiles, 'localField': localProfiles, 'foreignField': foreignProfiles, 'as': newProfileName}},\
    {"$unwind":f"${newProfileName}"},\
    {'$lookup': {'from': locations, 'localField': localLocation, 'foreignField': foreignLocation, 'as': newLocationName}},\
    {"$unwind":f"${newProfileName}"},\
    {"$match":{newProfileName: {"$exists":True}, newLocationName:{"$exists":True}}},\
    {"$project":{f"{newProfileName}.description":0, "sid_profile":0, f"{newProfileName}.sid":0, f"{newProfileName}.description":0, f"{newLocationName}.zip":0, \
    f"{newLocationName}.phone":0, f"{newLocationName}.blurb":0}},\
    {'$merge': {'into': collection_name, 'whenMatched': 'replace', 'whenNotMatched': 'insert'}}], allowDiskUse=True)
    
def outCollections(collection, profiles: str, locations: str, collection_name: str, localProfiles: str, foreignProfiles: str,
              newProfileName: str, localLocation: str, foreignLocation: str, newLocationName: str, sample: int):
    """
    The function performs an aggregate operation on the provided collection and exports the result to a new collection 
    with the specified name `collection_name`. The operation includes a sample of the collection with size `sample` documents 
    and join the collection with two other collections `profiles`, and `locations` based on the `localField` and `foreignField`
    and rename them with `newProfileName` and `newLocationName` respectively. The function also projects some fields and 
    hides some.

    Parameters:
        collection: a pymongo Collection object
        profiles (str): name of the collection that should be joined as profiles
        locations (str): name of the collection that should be joined as locations
        collection_name (str): the name of the new collection that should be created
        localProfiles (str): the field on the collection that is used as the join field with profiles collection
        foreignProfiles (str): the field on the profiles collection that is used as the join field
        newProfileName (str): the name of the array that contains the joined profile documents
        localLocation (str): the field on the collection that is used as the join field with locations collection
        foreignLocation (str): the field on the location collection that is used as the join field
        newLocationName (str): the name of the array that contains the joined location documents
        sample (int): the number of documents to be sampled
    """
    collection.aggregate([{"$sample": {"size":sample}},\
    {'$lookup': {'from': profiles, 'localField': localProfiles, 'foreignField': foreignProfiles, 'as': newProfileName}},\
    {"$unwind":f"${newProfileName}"},\
    {'$lookup': {'from': locations, 'localField': localLocation, 'foreignField': foreignLocation, 'as': newLocationName}},\
    {"$unwind":f"${newProfileName}"},\
    {"$match":{newProfileName: {"$exists":True}, newLocationName:{"$exists":True}}},\
    {"$project":{f"{newProfileName}.description":0, "sid_profile":0, f"{newProfileName}.sid":0, f"{newProfileName}.description":0, f"{newLocationName}.zip":0, \
    f"{newLocationName}.phone":0, f"{newLocationName}.blurb":0}},\
    {'$out': collection_name}], allowDiskUse=True)

def checkExistingCollection(database, collection_name: str):
    """
    The function check the existence of a collection with the specified name, and if it already exists, it will drop it.

    Parameters:
        database: a pymongo Database object
        collection_name (str): the name of the collection to check for existence
    """
    try:
        database.validate_collection(collection_name)
        print(f"\n{collection_name} collection exists\nDeleting")
        database[collection_name].drop()
    except: 
        print(f"\n{collection_name} collection doesn't exist")