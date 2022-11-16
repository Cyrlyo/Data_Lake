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
    
    args = parser.parse_args()
    
    return args.init_manually, args.download, args.maria_import, args.mongo_import, \
        args.database_import

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
