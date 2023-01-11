import pandas as pd
import os
import mechanize
import time
from mechanize import Browser
from typing import Tuple
from pandas import DataFrame
try:
    from import_data.utils_import import deletingFiles, deplaceFiles, createFile, unZip
except:
    from utils_import import deletingFiles, deplaceFiles, createFile, unZip
from os.path import join

def dataDownloader(url: str, file_name: list) -> Tuple[list, Browser]:
    """_summary_

    Args:
        url (str): _description_

    Returns:
        Tuple[list, Browser]: _description_
    """
    
    br = mechanize.Browser()
    br.open(url)
    
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

def mainDL(url: str, file_name: list) -> None:
    """_summary_

    Args:
        url (str): _description_
    """

    files, br = dataDownloader(url, file_name)

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
    

def poiImport(dataset_name: str, source: str, files_name: list) -> None:
    """
    The function imports a dataset of files, and store it in the "Data/Raw" directory.
    The function create a "Data" directory, a "Raw" directory, and a "Documentation" directory
    in the current working directory if they don't exist yet.
    Download files from dataset name and files list and unzip the files from the source url
    delete the downloaded zip files from source 
    and move the 'readme.txt' to the "Documentation" directory.
    
    Parameters:
        dataset_name (str) : name of dataset
        source (str) : url of zip file containing files
        files_name (list) : list of files to download
    """
    createFile("Data", os.getcwd())
    createFile("Raw", "Data")
    
    os.chdir("./Data/Raw")
    mainDL(dataset_name, files_name)
    unZip([source])
    
    deletingFiles(source)
    deplaceFiles("readme.txt", "../Documentation")
    
    os.chdir("../../")