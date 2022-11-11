import pandas as pd
import os
import mechanize
import time
from mechanize import Browser
from typing import Tuple
from pandas import DataFrame
from utils import deletingFiles, deplaceFiles, createFile, unZip
from os.path import join

def dataDownloader(url: str) -> Tuple[list, Browser]:
    """_summary_

    Args:
        url (str): _description_

    Returns:
        Tuple[list, Browser]: _description_
    """
    
    br = mechanize.Browser()
    br.open(url)
    
    file_name =["allCountries.zip", "readme.txt"]
    
    myfiles = []
    
    for link in br.links():
        for t in file_name:
            if t in str(link):
                myfiles.append(link)

    return myfiles, br

def downloadLink(link, br) -> None:
    """_summary_

    Args:
        link (_type_): _description_
        br (_type_): _description_
    """
    
    print(f"\nDownloading {link.text}... Please wait")
    f = open(link.text, "w")
    br.retrieve(link.base_url + link.url, filename=link.text)[0]
    f.close()
    print(link.text," has been downloaded")

def mainDL(url: str) -> None:
    """_summary_

    Args:
        url (str): _description_
    """

    files, br = dataDownloader(url)

    for link in files:
        time.sleep(1)
        try:
            downloadLink(link, br)
        except:
            pass

def importData(url: str) -> DataFrame:
    """_summary_

    Args:
        url (str): _description_

    Returns:
        _type_: _description_
    """
    
    data = pd.read_html(url)
    
    return data
    

def poi_import(dataset_name: str, source: str):
    """_summary_

    Args:
        source (str): _description_
    """
    createFile("Data", os.getcwd())
    createFile("Raw", "Data")
    
    os.chdir("./Data/Raw")
    mainDL(dataset_name)
    unZip([source])
    
    deletingFiles(source)
    deplaceFiles("readme.txt", "../Documentation")
    
    os.chdir("../../")