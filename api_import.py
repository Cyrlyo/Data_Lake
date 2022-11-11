import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import os, subprocess
from importation import unZip, deletingFiles
from utils import unZipper

api = KaggleApi()
api.authenticate()
api.dataset_download_file("shmalex/instagram-dataset",
                          file_name="instagram_locations.csv",
                          path="./Data/Raw")

unZipper("instagram_locations.csv.zip", path="./Data/Raw", end_dir="instagram_location")
deletingFiles("./Data/Raw/instagram_locations.csv.zip")