import csv
import json
import os
from pathlib import Path

def csvToJson(csv_path_file: str, json_path_file: str):
    """_summary_

    Args:
        csv_path_file (str): _description_
        json_path_file (str): _description_
    """
    
    json_array = []
    
    with open(csv_path_file, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter="\t")
        
        for row in csv_reader:
            json_array.append(row)
    print("\nExtracting json... please wait\nIt can take time")
    
    result, createPath = pathChecker(json_path_file)
    if not result:
        os.makedirs(createPath)
    
    with open(json_path_file, "w", encoding="utf-8") as json_file:
        json_string = json.dumps(json_array, ensure_ascii=False)
        json_file.write(json_string)

def pathChecker(path: str) -> bool:
    """_summary_

    Args:
        path (str): _description_

    Returns:
        bool: _description_
    """
    
    result_dict = {True: "exists", False: "doesn't exist"}
    
    splited_path = Path(path).parts
    formated_path = os.path.join(*splited_path[: -1])
    result = os.path.exists(formated_path)
    print(f"\n{formated_path} {result_dict[result]}")
    
    return result, formated_path