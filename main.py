from import_data.importation import poiImport
from import_data.api_import import apiImport
from kaggle.api import KaggleApi
from mariaDB.maria_import import importToMariaDB
from import_data.import_posts import importPosts
import argparse

DATASET_NAME = "shmalex/instagram-dataset"
SOURCE_1 = "instagram_locations.csv"
SOURCE_2 = "instagram_profiles.csv"
SOURCES = [SOURCE_1, SOURCE_2]
DATASET_NAME_2 = "http://download.geonames.org/export/dump"
SOURCE_3 = "allCountries.zip"
FILES_NAME = ["allCountries.zip", "readme.txt"]
DATASET_NAME_3 = "http://d3smaster.fr"
SOURCE_4 = "posts_reduced.zip"

def parse_arguements() -> bool:
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--init_manually", action="store_false", help="Download data & import them on databaes")
    parser.add_argument("-d", "--download", action="store_true", help="Only download data")
    parser.add_argument("-i", "--maria_import", action="store_true", help="Only import datas on MariaDB database")
    parser.add_argument("-m", "--mongo_import", action="store_true", help="Only import data on MongoDB database")
    parser.add_argument("-o", "--database_import", action="store_true", help="Import on MariaDB & MongoDB")
    
    args = parser.parse_args()
    return args.init_manually, args.download, args.maria_import, args.mongo_import, \
        args.database_import


if __name__ == "__main__":

    (init_manually, download, maria_import, mongo_import, database_import) = parse_arguements()
    
    table_name = SOURCE_3.replace(".zip", "")
    createtable_query = f"CREATE TABLE {table_name}(geonameid BIGINT NOT NULL UNIQUE PRIMARY KEY,\
    name VARCHAR(200) COLLATE utf8_general_ci, asciiname VARCHAR(200), alternatenames VARCHAR(10000),\
    latitude FLOAT, longitude FLOAT, feature_class CHAR(1), feature_code VARCHAR(10), country_code VARCHAR(255),\
    cc2 VARCHAR(255), admin1_code VARCHAR(20), admin2_code VARCHAR(80), admin3_code VARCHAR(20),\
    admin4_code VARCHAR(20), population BIGINT, elevation FLOAT, dem INT, timezone VARCHAR(40), modification_date DATE)"
    
    
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
        importToMariaDB("point_of_interest", table_name, "./Data/Raw/allCountries/allCountries.txt", createtable_query)