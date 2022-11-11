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