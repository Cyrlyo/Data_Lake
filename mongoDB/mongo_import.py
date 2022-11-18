try:
    from mongoDB.utils_mongo import csvToJson, mongoQueryLoad, connectToMongo, mongoPythonLoad
except:
    from utils_mongo import csvToJson, mongoQueryLoad, connectToMongo, mongoPythonLoad
import os
from os.path import join


def formatInstagram(current_data_path: str, target_data_path: str):
    
    listed = os.listdir(current_data_path)

    for liste in listed:
        if "instagram" in liste:
            temp_path = join(current_data_path, liste)
            file = os.listdir(temp_path)
            full_temp_path = join(temp_path, file[0])

            full_end_path = join(join(target_data_path, liste), file[0].replace(".csv", ".json"))

            csvToJson(full_temp_path, full_end_path)

def mongoImportLoadData(data_path: str, database_name: str, host: str, port: int):
    
    dir_list = os.listdir(data_path)
    
    for dir in dir_list:
        files = os.listdir(join(data_path, dir))
        
        for file in files:
            temp_name = file.replace(".json", "")
            colletion_name = temp_name.replace(f'{database_name}_', "")
            final_path = join(join(data_path, dir), file)
            
            print(f"\nImporting '{colletion_name}...'")
            mongoQueryLoad(database_name, colletion_name, host, port, final_path)
            print("Done")

def mongoPythonLoadData(data_path: str, database_name: str, host: str, port: int):
    
    client, db = connectToMongo(host, port, database_name)
    
    dir_list = os.listdir(data_path)
    
    for dir in dir_list:
        files = os.listdir(join(data_path, dir))
        
        for file in files:
            temp_name = file.replace(".json", "")
            colletion_name = temp_name.replace(f'{database_name}_', "")
            final_path = join(join(data_path, dir), file)
            
            collection = db[colletion_name]
            
            print(f"\nImporting '{colletion_name}...'")
            mongoPythonLoad(final_path, collection)