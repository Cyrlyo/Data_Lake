import mariadb
import yaml
from yaml.loader import SafeLoader
import sys
from typing import Dict
from mariadb.connections import Connection
from mariadb.cursors import Cursor
from mariadb import Error

def gettingCredentials() -> Dict:
    """_summary_

    Returns:
        Dict: _description_
    """
    
    try:
        with open("./mariaDB/credentials.yaml", "r") as creds:
            credentials = yaml.load(creds, Loader=SafeLoader)

    except:
        print("\nCreating credentials.yaml files. Please enter the following informations\n/!\ Don't share those informations /!\ ")
        user = input("Username: ")
        password = input("Password: ")
        host = input("host (by default localhost): ")
        port = int(input("port (by default 3306): "))

        credentials = {"user": user, "password": password, "host": host, "port":port}
        with open("./mariaDB/credentials.yaml", "w") as creds:
            yaml.dump(credentials, creds)
    
    return credentials
    
def connectToDatabase(credentials: dict) -> Connection:
    """_summary_

    Args:
        credentials (dict): _description_

    Returns:
        Connection: _description_
    """
    
    print("\nConnecting to the database...")
    try:
        connexion = mariadb.connect(
            user = credentials['user'],
            password = credentials["password"],
            host = credentials["host"],
            port = credentials["port"]
        )
    except Error as error:
        print(f"\nError connecting to the database: {error}")
        sys.exit(1)
    print("Done")

    return connexion

def listingDatabase(cursor: Cursor) -> None:
    """_summary_

    Args:
        cursor (Cursor): _description_
    """
    
    print("\nListing existing databases: ")
    cursor.execute("SHOW DATABASES")

    data_base_list = cursor.fetchall()
    
    for database in data_base_list:
        print(f"- {database[0]}")

def createDatabase(cursor: Cursor, database_name: str) -> None:
    """_summary_

    Args:
        cursor (Cursor): _description_
        database_name (str): _description_
    """
    # TODO: mettre un statement if exists delete or use avec argparse
    try:
        cursor.execute("CREATE DATABASE " + database_name + " CHARACTER SET utf8 COLLATE utf8_general_ci")
        print(f"\n{database_name} has been created")
    except Error as error:
        print(f"\n{error}")
    
def dropDatabase(cursor: Cursor, database_name: str):
    """

    Args:
        cursor (Cursor): _description_
        database_name (str): _description_
    """
    
    confirm = input(f"\nAre you sure to delete {database_name} enter [Y or N]: ")
    if confirm == "Y":
        try:
            cursor.execute("DROP DATABASE " + database_name)
            print(f"{database_name} has been deleted")
        except Error as error:
            print(f"Error: {error}")
    else:
        print(f"Drop {database_name} database has been canceled")

def useWorkplace(cursor: Cursor, database_name: str):
    """_summary_

    Args:
        cursor (Cursor): _description_
        database_name (str): _description_
    """
    
    try:
        cursor.execute("USE " + database_name)
    except Error as error:
        print(f"\nError: {error}")


    #TODO: Add docstrings & documentation