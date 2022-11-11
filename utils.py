import os, zipfile
from os.path import join
import shutil

def unZipper(file_name: str, path: str = None, end_dir: str = None ):
    """_summary_

    Args:
        file_name (str): _description_
        path (str, optional): _description_. Defaults to None.
        end_dir (str, optional): _description_. Defaults to None.
    """
    
    current_dir = os.getcwd()
    
    if path is not None:
        os.chdir(path)
    
    print("\nUnzipping...")
    if end_dir is not None:
        with zipfile.ZipFile(os.path.join(os.getcwd(), file_name), 'r') as zipref:
            zipref.extractall(end_dir)
        
    else:
        with zipfile.ZipFile(os.path.join(os.getcwd(), file_name), 'r') as zipref:
            zipref.extractall()
    print(f"{file_name} succesfully unzipped")
    
    os.chdir(current_dir)

def deplaceFiles(file_name: str, new_folder_path: str) -> None:
    """_summary_

    Args:
        file_name (str): _description_
        new_folder_path (str): _description_
    """
    try:
        shutil.move(join(os.getcwd(), file_name), join(new_folder_path, file_name))

    except:
        os.mkdir(new_folder_path)
        shutil.move(join(os.getcwd(), file_name), join(new_folder_path, file_name))

def deletingFiles(file_name: str) -> None:
    """_summary_

    Args:
        file_name (str): _description_
    """
    print(f"Deleting {file_name}")
    os.remove(file_name)
    
def createFile(folder_name: str, parent_dir: str):
    """_summary_

    Args:
        folder_name (str): Name of the new folder
        parent_dir (str): if the parent directory isn't the current file. If they are identical please pass 'os.getwd()'
    """
    print()
    current_dir = os.getcwd()
    print(f"You're current directory is: {current_dir}")
    path = join(join(current_dir, parent_dir), folder_name)
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
                with zipfile.ZipFile(join(os.getcwd(), file), 'r') as zip_ref:
                    zip_ref.extractall(f"{file_name[0][:-4]}")
                    print("Unzipping done")