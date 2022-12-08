import argparse
import os
from typing import List

def parse_arguements() -> bool:
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--init_manually", action="store_false", help="Download data & import them on databaes")
    parser.add_argument("-d", "--download", action="store_true", help="Only download data")
    parser.add_argument("-i", "--maria_import", action="store_true", help="Only import datas on MariaDB database")
    parser.add_argument("-m", "--mongo_import", action="store_true", help="Only import data on MongoDB database")
    parser.add_argument("-o", "--database_import", action="store_true", help="Import on MariaDB & MongoDB")
    parser.add_argument("-f", '--format_data', action="store_true", help="Format data (csv to json)")
    parser.add_argument("-p", "--python_loader", action="store_true", help="Use python loader for \
        MongoDB datas. USE ONLY IF NECESSARY! IT'S VERY LONG! About 30 min to 1 hour \
            per document!")
    parser.add_argument("--data_prep", action="store_true", help="Prepare instagram data on MongoDB")
    parser.add_argument("--quick_prep", action="store_false", help="Only prepare some data (full takes 1h to run)")
    parser.add_argument("--only_merge", action="store_false", help="Only merge collections as data preparation")
    parser.add_argument("--enbale_merge", action="store_true", help="Enable merge collections while preparing datas")
    parser.add_argument("--sample", type=int, default=150000, help="Number of document to merge")
    parser.add_argument("--demo", action="store_true", help="Disable demo mode")
    
    args = parser.parse_args()
    
    return args.init_manually, args.download, args.maria_import, args.mongo_import, \
        args.database_import, args.format_data, args.python_loader, args.data_prep, \
        args.quick_prep, args.only_merge, args.enbale_merge, args.sample, args.demo

def collectSQLQuery(path: str) -> dict:
    """_summary_

    Args:
        path (str): _description_

    Returns:
        List[str]: _description_
    """
    
    files = os.listdir(path)
    
    query_dict = {}
    for file in files:
        query_dict[str(file).replace(".sql", "")] = open(os.path.join(path, file), "r").read().replace("\n", "")
        
    return query_dict
