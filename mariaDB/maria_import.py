import mariadb
import yaml
from yaml.loader import SafeLoader
import sys
from typing import Dict
from mariadb.connections import Connection

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

def testingConnexion(connexion: Connection):
    
    cursor = connexion.cursor()
    print("\nListing existing databases: ")
    cursor.execute("SHOW DATABASES")

    data_base_list = cursor.fetchall()
    
    for database in data_base_list:
        print(f"- {database[0]}")


if __name__ == "__main__":
    
    credentials = gettingCredentials()
    connexion = connectToDatabase(credentials)
    testingConnexion(connexion)