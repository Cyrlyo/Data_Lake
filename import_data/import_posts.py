import os
try: 
    from import_data.importation import mainDL
    from import_data.utils_import import unZip, deletingFiles
except:
    from importation import mainDL
    from utils_import import unZip, deletingFiles
    
def importPosts(dataset_name: str, source: str, files_name: list):
    os.chdir("./Data/Raw")
    mainDL(dataset_name, files_name)
    unZip([source])

    deletingFiles(source)
    os.chdir("../../")
