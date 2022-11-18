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

# formatInstagram("./Data/Raw", "./Data/Formated")