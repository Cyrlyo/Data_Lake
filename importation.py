import pandas as pd
import numpy as np
import random
import lxml
import requests
import zipfile
import os, sys, glob

def importData(url: str):
    
    data = pd.read_html(url)
    
    return data

def createFile(folder_name: str, parent_dir: str):
    
    current_dir = os.getcwd()
    print(f"You're current directory is: {current_dir}")
    path = os.path.join(os.path.join(current_dir, parent_dir), folder_name)
    os.mkdir(path)
    print(f"'{folder_name}' has been created\nPath: {path}")
    

def importhtml(url: str):
    
    print("coucou1")
    response = requests.get(url)
    os.mkdir("Raw")
    print("coucou2")
    open("./Data/RAw/allCountries.zip", "wb").write(response.content)
    print("coucou3")


def unZip(file_name: list):
    """"
    arguments: 
    - file_name: a list of string of files' name with it extension we're looking for unzip.
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
    # print(test)
    
    createFile("Raw", "Data")
    # importhtml("http://download.geonames.org/export/dump/allCountries.zip")
    # unZip(["allCountries.zip"])
    