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

def importhtml(url: str):
    
    print("coucou1")
    response = requests.get(url)
    print("coucou2")
    open("allCountries.zip", "wb").write(response.content)
    print("coucou3")

def unZip(file_name: list):
    """"
    arguments: 
    - file_name: a list of string of files' name with it extension we're looking for unzip.
    """

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
    
    # importhtml("http://download.geonames.org/export/dump/allCountries.zip")
    unZip(["allCountries.zip"])
    