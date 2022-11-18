try:
    from mongoDB.utils_mongo import csvToJson
except:
    from utils_mongo import csvToJson
import os


def formatInstagram(current_data_path: str, target_data_path: str):
    
    listed = os.listdir(current_data_path)

    for liste in listed:
        if "instagram" in liste:
            temp_path = os.path.join(current_data_path, liste)
            file = os.listdir(temp_path)
            full_temp_path = os.path.join(temp_path, file[0])

            full_end_path = os.path.join(os.path.join(target_data_path, liste), file[0].replace(".csv", ".json"))

            csvToJson(full_temp_path, full_end_path)

def loadDataMongoImport(database_name: str, collection_name: str, host: str, port: int, file_path: str):
    """_summary_
    NEED MONGOIMPORT INSTALLED ON YOUR DEVICE§
    
    Args:
        database_name (str): _description_
        host (str): by default localhost i.e. 127.0.0.1
        port (int): by default 27017
        file_path (str): _description_
    """
    
    os.system(f'mongoimport --host {host} -d {database_name} --port {port}\
        --collection {collection_name} --file {file_path} --jsonArray ')
