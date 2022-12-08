import sys, os
from tqdm import tqdm
path = os.getcwd()
sys.path.append(path)

from mongoDB.utils_mongo import connectToMongo
from elasticsearch import Elasticsearch, helpers
from typing import List
from mariaDB.utils_maria import gettingCredentials, connectToDatabase, getMariaData

CREDENTIALS = gettingCredentials()
CONNEXON = connectToDatabase(CREDENTIALS)

try:
    es = Elasticsearch(hosts="http://localhost:9200")
except:
    print("Can't connect to ElastichSearch server. Please make sur it's running")

def catchDataMongo(collection, index_name: str) -> list:
    actions = []
    for data in tqdm(collection.find({}, {"cts":0, "profile.cts":0,"location.cts":0, "profile._id":0, "location._id":0}), total=collection.count_documents({})):
        data.pop('_id')
        action = {
                    "_index": index_name,
                    # "type": 'instagram_posts',
                    "_source": data
                }
        actions.append(action)
    return actions

def importToElastich(es: Elasticsearch, actions: list, index: str):

    res = es.indices.exists(index=index)
    if res:
        es.indices.delete(index=index)
    es.indices.create(index=index)
    helpers.bulk(es, actions, index=index, stats_only=True)

def elkImport(mongo_info: List, collection_name: str, mariadb_db_name: str, mariadb_table: str):
    
    print("\nImporting mongo datas")
    client, db = connectToMongo(mongo_info[0], mongo_info[1], mongo_info[2])
    collection = db[collection_name]
    actions = catchDataMongo(collection, collection_name)
    
    importToElastich(es, actions, collection_name)
    print("Done")
    
    print("\nImporting mariaDB datas into elasticsearch")
    cursor = CONNEXON.cursor(dictionary=True)
    res = getMariaData(cursor, mariadb_db_name, mariadb_table)
    importToElastich(es, res, mariadb_db_name)
    print("Done")