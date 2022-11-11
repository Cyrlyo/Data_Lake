import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import os, subprocess
from importation import unZip, deletingFiles
from utils import unZipper

print("coucou1")
api = KaggleApi()
api.authenticate()
print("coucou2")
api.dataset_download_file("shmalex/instagram-dataset",
                          file_name="instagram_locations.csv",
                          path="./Data/Raw")
print("coucou3")

# unZip("./Data/Raw/instagram_locations.csv.zip")
unZipper("instagram_locations.csv.zip", "./Data/Raw")
print("coucou4")
deletingFiles("./Data/Raw/instagram_locations.csv.zip")
print("coucou5")