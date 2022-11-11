from importation import main as poi_import
from api_import import main as api_import
from kaggle.api import KaggleApi

DATASET_NAME = "shmalex/instagram-dataset"
SOURCE_1 = "instagram_locations.csv"
SOURCE_2 = "instagram_profiles.csv"
SOURCES = [SOURCE_1, SOURCE_2]
DATASET_NAME_2 = "http://download.geonames.org/export/dump"
SOURCE_3 = "allCountries.zip"

try:
    API = KaggleApi()
    API.authenticate()
except:
    print("\nMake sure that you're kaggle.json file (containing username + api key) is stores on ${HOME}/.kaggle")

poi_import(DATASET_NAME_2, SOURCE_3)
api_import(API, DATASET_NAME, SOURCES)