import pandas as pd
import numpy as np
import random
import lxml
import requests
import zipfile
import os, sys, glob

def importData(url: str):
    """_summary_

    Args:
        url (str): _description_

    Returns:
        _type_: _description_
    """
    
    data = pd.read_html(url)
    
    return data

def createFile(folder_name: str, parent_dir: str):
    """_summary_

    Args:
        folder_name (str): Name of the new folder
        parent_dir (str): if the parent directory isn't the current file. If they are identical please pass 'os.getwd()'
    """
    print()
    current_dir = os.getcwd()
    print(f"You're current directory is: {current_dir}")
    path = os.path.join(os.path.join(current_dir, parent_dir), folder_name)
    try: 
        os.mkdir(path)
        print(f"'{folder_name}' has been created\nPath: {path}")
    except:
        print("Folder already exists")
    

def importhtml(url: str, path_dir: str):
    """_summary_

    Args:
        url (str): URL of the wanted file to download.
        dir (str): path directory of where you're want to download the file
    """
    
    print("coucou1")
    response = requests.get(url, allow_redirects=True, stream=True)
    print()
    
    print("coucou2")
    open(os.path.join(path_dir, "allCountries.zip"), "wb").write(response.content)
    print("coucou3")


def unZip(file_name: list):
    """_summary_

    Args:
        file_name (list): file_name: a list of string of files' name with it extension we're looking for unzip.
    """
    os.chdir("Data/Raw")
    files_name = os.listdir()
    extension = [".zip", ".tar.gz"]
    
    for file in files_name:
        if file[-4:] in extension:
            print(file)
            if file in file_name:
                with zipfile.ZipFile(os.path.join(os.getcwd(), file), 'r') as zip_ref:
                    zip_ref.extractall("./UnZipTest")
                    print("coucou2")


if __name__ == "__main__":
    
    # test = importData("https://www.kaggle.com/datasets/shmalex/instagram-dataset?select=instagram_locations.csv")
    
    createFile("Raw", "Data")
    importhtml("http://download.geonames.org/export/dump/allCountries.zip", "./Data/Raw")
    unZip(["allCountries.zip"])
    