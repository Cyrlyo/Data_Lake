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
    """
    The function returns a list of links that contains the files specified in file_name, and a browser object.

    Parameters:
        url (str) : the url where the files are located
        file_name (list) : the list of files to download

    Returns:
        Tuple[list, Browser]: a list of links of the files to download, and a browser object
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
    """
    The function downloads a file from a given link, and store it in the current working directory.

    Parameters:
        link : the link of the file
        br : the browser object that is used to access the link
    """
    
    print(f"\nDownloading {link.text}... Please wait")
    f = open(link.text, "w")
    br.retrieve(link.base_url + link.url, filename=link.text)[0]
    f.close()
    print(link.text," has been downloaded")

def mainDL(url: str, file_name: list) -> None:
    """
    The function downloads files from a given url, and store them in the current working directory.
    the function takes a list of files_name to download from the url.

    Parameters:
        url (str) : the url where the files are located
        file_name (list): a list of strings representing the files to download
    """

    files, br = dataDownloader(url, file_name)

    for link in files:
        time.sleep(1)
        try:
            downloadLink(link, br)
        except:
            pass

def importData(url: str) -> DataFrame:
    """
    The function import data from a given url and return it as a pandas DataFrame.

    Parameters:
        url (str): the url where the data is located
    
    Returns:
        DataFrame: a pandas DataFrame containing the imported data
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