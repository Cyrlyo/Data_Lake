import mariadb
import yaml
from yaml.loader import SafeLoader
import sys

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

cursor = connexion.cursor()
cursor.execute("SHOW DATABASES")

data_base_list = cursor.fetchall()
  
for database in data_base_list:
    print(database)