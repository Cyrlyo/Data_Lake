import sys, os
from tqdm import tqdm
path = os.getcwd()
sys.path.append(path)

from mongoDB.utils_mongo import connectToMongo
from elasticsearch import Elasticsearch, helpers

HOST = "localhost"
MONGO_PORT = 27017
MONGO_DATABASE_NAME = "instagram"


client, db = connectToMongo(HOST, MONGO_PORT, MONGO_DATABASE_NAME)
collection = db["posts_details_reduced"]

try:
    es = Elasticsearch(hosts="http://localhost:9200")
except:
    print("Can't connect to ElastichSearch server. Please make sur it's running")

def catchDataMongo(collection) -> list:
    actions = []
    for data in tqdm(collection.find({}, {"cts":0, "profile.cts":0,"location.cts":0, "profile._id":0, "location._id":0}), total=collection.count_documents({})):
        data.pop('_id')
        action = {
                    "_index": 'instagram_poi',
                    "type": 'instagram_posts',
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

