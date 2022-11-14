import mariadb
import yaml
from yaml.loader import SafeLoader
import sys
from typing import Dict
from mariadb.connections import Connection
from mariadb.cursors import Cursor

def gettingCredentials() -> Dict:
    
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
    
    print("\nConnecting to the database...")
    try:
        connexion = mariadb.connect(
            user = credentials['user'],
            password = credentials["password"],
            host = credentials["host"],
            port = credentials["port"]
        )
    except mariadb.Error as error:
        print(f"\nError connecting to the database: {error}")
        sys.exit(1)
    print("Done")

    return connexion

def listingDatabase(cursor: Cursor) -> None:
    
    print("\nListing existing databases: ")
    cursor.execute("SHOW DATABASES")

    data_base_list = cursor.fetchall()
    
    for database in data_base_list:
        print(f"- {database[0]}")

def createDatabase(cursor: Cursor, database_name: str) -> None:
    
    try:
        cursor.execute("CREATE DATABASE " + database_name)
        print(f"\n{database_name} has been created")
    except mariadb.Error as error:
        print(f"Error: {error}")
    
def dropDatabase(cursor: Cursor, database_name: str):
    
    confirm = input(f"\nAre you sure to delete {database_name} enter [Y or N]: ")
    if confirm == "Y":
        try:
            cursor.execute("DROP DATABASE " + database_name)
            print(f"{database_name} has been deleted")
        except mariadb.Error as error:
            print(f"Error: {error}")
    else:
        print(f"Drop {database_name} database has been canceled")

    # TODO: Mettre les fonction génériques dans un script 'utils' ou 'utils_db'
    #TODO: Add docstrings & documentation