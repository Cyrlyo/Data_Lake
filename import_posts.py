import os
from import_data.importation import mainDL
from import_data.utils import unZip, deletingFiles, deplaceFiles

def importPosts(dataset_name: str, source: str, files_name: list):
    os.chdir("./Data/Raw")
    mainDL(dataset_name, files_name)
    unZip([source])

    deletingFiles(source)
    os.chdir("../../")

# importPosts("http://d3smaster.fr", "posts_reduced.zip", ["posts_reduced.zip"])
