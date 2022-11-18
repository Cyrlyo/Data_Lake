import csv
import json

def csvToJson(csv_path_file: str, json_path_file: str):
    
    json_array = []
    
    # print(f"Opening {csv_path_file}")
    with open(csv_path_file, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter="\t")
        
        for row in csv_reader:
            json_array.append(row)
    print("\nExtracting json... please wait\nIt can take time")
    
    with open(json_path_file, "w", encoding="utf-8") as json_file:
        json_string = json.dumps(json_array, ensure_ascii=False)
        json_file.write(json_string)
        