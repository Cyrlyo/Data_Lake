import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import os, subprocess
from importation import unZip, deletingFiles
from utils import unZipper

DATASET_NAME = "shmalex/instagram-dataset"
SOURCE_1 = "instagram_locations.csv"
SOURCE_2 = "instagram_profiles.csv"

try:
    API = KaggleApi()
    API.authenticate()
except:
    print("\nMake sur that you're kaggle.json file (containing username + api key) is stores on $HOME/.kaggle")


def apiDownload(api: KaggleApi, dataset_name: str, source: str, folder: str):
    """_summary_

    Args:
        dataset_name (str): _description_
        source (str): _description_
        folder (str): _description_
    """
    
    api.dataset_download_file(dataset_name,
                          file_name=source,
                          path=folder)

def prepFile(file_name: str, file_extension: str, path: str, end_dir: str):
    """_summary_

    Args:
        file_name (str): _description_
        file_extension (str): _description_
        path (str): _description_
        end_dir (str): _description_
    """

    unZipper(file_name + file_extension, path, end_dir)
    deletingFiles(os.path.join(path, file_name + file_extension))

if __name__ == "__main__":
    
    apiDownload(API, DATASET_NAME, SOURCE_1, "./Data/Raw")
    prepFile(SOURCE_1, ".zip", "./Data/Raw", SOURCE_1[:-4])
    
    apiDownload(API, DATASET_NAME, SOURCE_2, "./Data/Raw")
    prepFile(SOURCE_2, ".zip", "./Data/Raw", SOURCE_2[:-4])