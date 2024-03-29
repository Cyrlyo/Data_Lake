from import_data.importation import poiImport
from import_data.api_import import apiImport
from kaggle.api import KaggleApi
from mariaDB.maria_import import importToMariaDB
from import_data.import_posts import importPosts
from utils import parse_arguements, collectSQLQuery
from mongoDB.mongo_import import formatInstagram, mongoImportLoadData, mongoPythonLoadData, deplacePostsDetailsReduced
from mongoDB.preparation import dataPreparation
from elk.utils_elk import elkImport
import time

DATASET_NAME = "shmalex/instagram-dataset"
DATASET_NAME_2 = "http://download.geonames.org/export/dump"
DATASET_NAME_3 = "http://d3smaster.fr"
DATASET_NAME_4 = "http://posts-data-storage.online"
SOURCE_1 = "instagram_locations.csv"
SOURCE_2 = "instagram_profiles.csv"
SOURCE_3 = "allCountries.zip"
SOURCE_4 = "instagram_posts_reduced.zip"
SOURCE_5 = "posts_details_reduced.zip"
SOURCES = [SOURCE_1, SOURCE_2]
FILES_NAME = ["allCountries.zip", "readme.txt"]
HOST = "localhost"
MONGO_PORT = 27017
MONGO_DATABASE_NAME = "instagram"


#TODO: Create folder "Query" and query.sql files with all queries\
# then .split(";") to have a list of queries
# Or make a dict with the query as value use os.listdir() to iterate on it and\ 
# use it to dict's keys

#TODO: Add "./Data/Raw" & "./Data/Formated" as environment variables? And as arguments in
# poiimport & apiImport?

#TODO: We'll probably need to move everything about downloading, preparing & importing data 
# in a function to after have space to have query elasticsearch & kibana queries & visualization
if __name__ == "__main__":

    (init_manually, download, maria_import, mongo_import,\
    database_import, format_data, python_loader, data_prep,\
    quick_prep, only_merge, enable_merge, sample, demo, elk) = parse_arguements()
    
    table_name_3 = SOURCE_3.replace(".zip", "")

    start_time = time.time()
    
    if init_manually or download:
        try:
            API = KaggleApi()
            API.authenticate()
        except:
            print("\nMake sure that your kaggle.json file (containing username + api key) is stored in $HOME/.kaggle")

        poiImport(DATASET_NAME_2, SOURCE_3, FILES_NAME)
        apiImport(API, DATASET_NAME, SOURCES)
        importPosts(DATASET_NAME_3, SOURCE_4, [SOURCE_4])
        importPosts(DATASET_NAME_4, SOURCE_5, [SOURCE_5])
    
    if init_manually or format_data:
        formatInstagram("./Data/Raw", "./Data/Formated")
        deplacePostsDetailsReduced("./Data/Raw/posts_details_reduced", "./Data/Formated/posts_details_reduced")

    if init_manually or maria_import or database_import:
        query_dict = collectSQLQuery("./query/load_data")
        importToMariaDB("point_of_interest", table_name_3, "./Data/Raw/allCountries/allCountries.txt", query_dict[table_name_3])
    
    if init_manually or mongo_import or database_import:
        if not python_loader:
            mongoImportLoadData("./Data/Formated", MONGO_DATABASE_NAME, HOST, MONGO_PORT)
        else:
            mongoPythonLoadData("./Data/Formated", MONGO_DATABASE_NAME, HOST, MONGO_PORT)
    
    if demo:
        if init_manually or data_prep:
            dataPreparation(HOST, MONGO_PORT, MONGO_DATABASE_NAME, "posts_details", quick_prep, only_merge, enable_merge, sample)
    
    if elk:
        elkImport([HOST, MONGO_PORT, MONGO_DATABASE_NAME], "posts_details_reduced", "point_of_interest", table_name_3.lower())
    
    delta_time = time.time() - start_time
    print(f"Execution time: {time.strftime('%H:%M:%S', time.gmtime(delta_time))}")