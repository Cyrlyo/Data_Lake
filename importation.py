import pandas as pd
import numpy as np
import random
import lxml
import requests
import zipfile
import os, sys, glob
import mechanize
import time
from mechanize import Browser
from typing import Tuple
from pandas import DataFrame
import shutil

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
        print(f"{folder_name} has been created\nPath: {path}")
    except:
        print("Folder already exists")


def unZip(file_name: list):
    """_summary_

    Args:
        file_name (list): file_name: a list of string of files' name with it extension we're looking for unzip.
    """
    files_name = os.listdir()
    extension = [".zip", ".tar.gz"]
    
    for file in files_name:
        if file[-4:] in extension:
            print(f"\nUnzipping {file}")
            if file in file_name:
                with zipfile.ZipFile(os.path.join(os.getcwd(), file), 'r') as zip_ref:
                    zip_ref.extractall(f"{file_name[0][:-4]}")
                    print("Unzipping done")

    
def deplaceFiles(file_name: str, new_folder_path: str) -> None:
    """_summary_

    Args:
        file_name (str): _description_
        new_folder_path (str): _description_
    """
    try:
        shutil.move(os.path.join(os.getcwd(), file_name), os.path.join(new_folder_path, file_name))

    except:
        os.mkdir(new_folder_path)
        shutil.move(os.path.join(os.getcwd(), file_name), os.path.join(new_folder_path, file_name))

def deletingFiles(file_name: str) -> None:
    """_summary_

    Args:
        file_name (str): _description_
    """
    print(f"Deleting {file_name}")
    os.remove(file_name)
    

def main():
    
    createFile("Data", os.getcwd())
    createFile("Raw", "Data")
    
    os.chdir("./Data/Raw")
    mainDL("http://download.geonames.org/export/dump")
    unZip(["allCountries.zip"])
    
    deletingFiles("allCountries.zip")
    deplaceFiles("readme.txt", "../Documentation")
    
    os.chdir("../../")
    

if __name__ == "__main__":
    
    main()