import pandas as pd
import numpy as np
import random
import lxml
import requests

def importData(url: str):
    
    data = pd.read_html(url)
    
    return data

def importhtml(url: str):
    
    print("coucou1")
    response = requests.get(url)
    print("coucou2")
    open("allCountries.zip", "wb").write(response.content)
    print("coucou3")


if __name__ == "__main__":
    
    print("coucou")
    # test = importData("https://www.kaggle.com/datasets/shmalex/instagram-dataset?select=instagram_locations.csv")
    # print(test)
    
    importhtml("http://download.geonames.org/export/dump/allCountries.zip")
    