import mariadb
import os
from mariadb.cursors import Cursor
from mariadb.connections import Connection
from mariaDB.utils_maria import gettingCredentials, connectToDatabase, listingDatabase, \
    createDatabase, useWorkplace, createTable


def importData(connexion: Connection, cursor: Cursor, data_path: str, table_name: str) -> None:
    """_summary_

    Args:
        connexion (Connection): Connection object to the database
        cursor (Cursor): MariaDB Cursor object
        data_path (str): path to the data to import in MariaDB (here ./Data/Raw/allCountries/allCountries.zip)
        table_name (str): table's name
    """
    try:
        path = os.getcwd()
        all_path = os.path.join(path, data_path)
        all_path = all_path.replace(os.sep, "/")
        all_path = all_path.replace("/.", "")
        
        print("\nImporting data... Please wait")
        cursor.execute(f"LOAD DATA LOCAL INFILE '{all_path}' INTO TABLE {table_name} FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n'")
        print("Done")
    except mariadb.Error as error:
        print(f"Error: {error}")

    connexion.commit()
    cursor.closed

def importToMariaDB(database_name: str, table_name: str, data_path: str, createtable_query: str) -> None:
    """
    The function imports data from a file located in data_path and stores it in a MariaDB table.
    It also creates the database and the table if they do not exist yet.

    Parameters:
        database_name (str): the name of the database where the data will be stored
        table_name (str): the name of the table where the data will be stored
        data_path (str): the path of the file where the data is located
        createtable_query (str): a SQL query to create the table
    """
    #TODO: Rename this function for allCountriesImportMariaDB or something like this

    credentials = gettingCredentials()
    connexion = connectToDatabase(credentials)
    
    cursor = connexion.cursor()
    
    listingDatabase(cursor)
    createDatabase(cursor, database_name)
    useWorkplace(cursor, database_name)
    
    createTable(connexion, table_name, createtable_query)
    importData(connexion, cursor, data_path, table_name)
    
    cursor.close()
    connexion.close()
