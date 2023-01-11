import mariadb
import yaml
from yaml.loader import SafeLoader
import sys
from typing import Dict
from mariadb.connections import Connection
from mariadb.cursors import Cursor
from mariadb import Error

def gettingCredentials() -> Dict:
    """
    Read and import credentials store in credentials.yaml.
    Don't share your password. Add credentials.yaml in .gitignore.

    Returns:
        Dict: contains you're MariaDB profil credentials
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
    """
    Connect to MariaDB. 

    Args:
        credentials (dict): Credentials of you're local MariaDB profil. 
            DON'T SHARE YOUR PASSWORD!
            By default : 
                - user : "root"
                - host : "localhost" or "127.0.0.1"
                - port : "3306"

    Returns:
        Connection: MariaDB Connection
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
    """
    Listing existing MariaDB databases.

    Args:
        cursor (Cursor): MariaDB Cursor
    """
    
    print("\nListing existing databases: ")
    cursor.execute("SHOW DATABASES")

    data_base_list = cursor.fetchall()
    
    for database in data_base_list:
        print(f"- {database[0]}")

def createDatabase(cursor: Cursor, database_name: str) -> None:
    """
    We set by default UTF-8 encoding to correctly parse accents.

    Args:
        cursor (Cursor): MariaDB Cursor
        database_name (str): Database's name to create
    """
    try:
        cursor.execute("CREATE DATABASE %s CHARACTER SET utf8 COLLATE utf8_general_ci" % database_name)
        print(f"\n{database_name} has been created")
    except Error as error:
        print(f"\n{error}")
    
def dropDatabase(cursor: Cursor, database_name: str):
    """

    Args:
        cursor (Cursor): MariaDB Cursos
        database_name (str): database's name to delete
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
    """
    Select a MariaDB database on which we'll work.

    Args:
        cursor (Cursor): MariaDB Cursor
        database_name (str): database name on which we'll work
    """
    
    try:
        cursor.execute("USE " + database_name)
    except Error as error:
        print(f"\nError: {error}")

def collectColumnNames(path: str) -> list[str]:
    """
    The function reads the first line of a file specified by the `path` 
    and returns it as a list after removing quotes, newlines and splitting it by tab.
    
    Parameters:
        path (str): the path to the file to read the first line from
    
    Returns:
        List: the first line of the file as a list 
    """
    
    with open(path, encoding="utf8", newline="\n") as file:
        first_line = file.readline()
    
    first_line = first_line.replace('"', "")
    first_line = first_line.replace("\n", "")
    first_line = first_line.split("\t")

    return first_line

def createTable(connexion: Connection, table_name: str, createtable_query: str) -> None:
    """_summary_
    If the table already exists the current one will be deleted and replace by the new one.
    Args:
        connexion (Connection): _description_
        table_name (str): _description_
    """
    cursor = connexion.cursor()
    cursor.execute("DROP TABLE IF EXISTS %s" % table_name)

    try:
        print("Creating table %s (if already existing has been deleted and recreated)" % table_name)
        cursor.execute(createtable_query)
    except mariadb.Error as error:
        print(f"Error: {error}")

        cursor.close()

def getMariaData(cursor: Cursor, database_name: str, table_name) -> list:
    
    number = countDocuments(cursor, database_name, table_name)
    
    useWorkplace(cursor, database_name)
    query = "SELECT name, slug, lat, lng, cd, dem FROM %s"% table_name
    cursor.execute(query)
    print("\nFetching datas...")
    res = cursor.fetchmany(number["count"])
    # res = cursor.fetchall()
    print("Data fetched")
    
    return res

def countDocuments(cursor: Cursor, database_name: str, table_name):
    
    useWorkplace(cursor, database_name)
    cursor.execute("SELECT count(*) as count FROM %s"% table_name)
    res = cursor.fetchall()
    return res[0]