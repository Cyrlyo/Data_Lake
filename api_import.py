from kaggle.api.kaggle_api_extended import KaggleApi
import os
from utils import unZipper, deletingFiles


def apiDownload(api: KaggleApi, dataset_name: str, source: str, folder: str):
    """_summary_

    Args:
        dataset_name (str): name of the dataset on kaggle
        source (str): name of the file on kaggle
        folder (str): path of the folder where you want to download the file
    """
    
    api.dataset_download_file(dataset_name,
                          file_name=source,
                          path=folder)

def prepFile(file_name: str, file_extension: str, path: str, end_dir: str):
    """_summary_

    Args:
        file_name (str): name of the file to prepare
        file_extension (str): .zip or other zipped extensions
        path (str): path where the file is stored
        end_dir (str): path where the unzipped file should be stored
    """

    unZipper(file_name + file_extension, path, end_dir)
    deletingFiles(os.path.join(path, file_name + file_extension))

def api_import(api: KaggleApi, dataset: str, sources: list):
    
    for source in sources:
        print(f"\nDownloading {source}... Please wait")
        apiDownload(api, dataset, source, "./Data/Raw")
        prepFile(source, ".zip", "./Data/Raw", source[:-4])
        print("Done")
