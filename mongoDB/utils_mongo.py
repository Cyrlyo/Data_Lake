import csv
import json
import os
from pathlib import Path
from pymongo import MongoClient
from tqdm import tqdm

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
    """_summary_
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
    """_summary_
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

def countEmptyString(collection, variable: str):
    
    results = collection.aggregate([{"$match": {variable: {"$eq": ""}}}, {"$group": {"_id": "null", "count": {"$sum": 1}}}])
    for result in results:
        print(f"Number of null string in '{variable}': {result[list(result.keys())[-1]]}")

def strToDate(collection, variable: str):
    
    collection.update_many({variable: {"$type": "string", "$ne": ""}}, [{"$set": {variable: {"$convert": {"input": "$%s"% variable, "to": "date"}}}}])

def merge(collection_receive, collection_give: str, receive_field: str, give_file: str, new_field_name: str, database_name: str, collection_name: str):
    
    collection_receive.aggregate([{"$lookup": {"from":"%s"% collection_give, "localField":"%s"% receive_field,\
        "foreignField":"%s"% give_file, "as":"%s"% new_field_name}}, {"$merge": {"$into": {"db": "%s"% database_name, "coll": "%s"% collection_name}}}])