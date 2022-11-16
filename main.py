from import_data.importation import poiImport
from import_data.api_import import apiImport
from kaggle.api import KaggleApi
from mariaDB.maria_import import importToMariaDB
from import_data.import_posts import importPosts
from utils import parse_arguements, collectSQLQuery

DATASET_NAME = "shmalex/instagram-dataset"
SOURCE_1 = "instagram_locations.csv"
SOURCE_2 = "instagram_profiles.csv"
SOURCES = [SOURCE_1, SOURCE_2]
DATASET_NAME_2 = "http://download.geonames.org/export/dump"
SOURCE_3 = "allCountries.zip"
FILES_NAME = ["allCountries.zip", "readme.txt"]
DATASET_NAME_3 = "http://d3smaster.fr"
SOURCE_4 = "posts_reduced.zip"

#TODO: Create folder "Query" and query.sql files with all queries\
# then .split(";") to have a list of queries
# Or make a dict with the query as value use os.listdir() to iterate on it and\ 
# use it to dict's keys

if __name__ == "__main__":

    (init_manually, download, maria_import, mongo_import, database_import) = parse_arguements()
    
    query_dict = collectSQLQuery("./query/load_data")
    
    table_name_3 = SOURCE_3.replace(".zip", "")

    
    if init_manually or download:
        try:
            API = KaggleApi()
            API.authenticate()
        except:
            print("\nMake sure that you're kaggle.json file (containing username + api key) is stored in $HOME/.kaggle")

        poiImport(DATASET_NAME_2, SOURCE_3, FILES_NAME)
        apiImport(API, DATASET_NAME, SOURCES)
        importPosts(DATASET_NAME_3, SOURCE_4, [SOURCE_4])

    if init_manually or maria_import or database_import:
        importToMariaDB("point_of_interest", table_name, "./Data/Raw/allCountries/allCountries.txt", query_dict[table_name_3])