import mariadb
import pandas as pd
import os
from os.path import join
from mariadb.cursors import Cursor
from mariadb.connections import Connection
from utils_db import gettingCredentials, connectToDatabase, listingDatabase, \
    createDatabase, dropDatabase, useWorkplace

def createTable(connexion: Connection, table_name: str):
    
    cursor = connexion.cursor()
    cursor.execute("DROP TABLE IF EXISTS test")
    #TODO: Do a F-string and add table_name as argument and print(importing data)
    createtable_query = f"CREATE TABLE {table_name}(geonameid BIGINT NOT NULL UNIQUE PRIMARY KEY,\
        name VARCHAR(200) COLLATE utf8_general_ci, asciiname VARCHAR(200), alternatenames VARCHAR(10000),\
            latitude FLOAT, longitude FLOAT, feature_class CHAR(1), feature_code VARCHAR(10), country_code VARCHAR(255),\
                cc2 VARCHAR(255), admin1_code VARCHAR(20), admin2_code VARCHAR(80), admin3_code VARCHAR(20),\
                    admin4_code VARCHAR(20), population BIGINT, elevation FLOAT, dem INT, timezone VARCHAR(40), modification_date DATE)"
    
    try:
        cursor.execute(createtable_query)
    except mariadb.Error as error:
        print(f"Error: {error}")

def importData(cursor: Cursor, data_path: str, table_name: str):
    # We should have 12350210 rows
    try:
        path = os.getcwd()
        all_path = os.path.join(path, data_path)
        all_path = all_path.replace(os.sep, "/")
        all_path = all_path.replace("/.", "")
        
        print("\nImporting data... Please wait")
        # cursor.execute(f"LOAD DATA LOCAL INFILE '{all_path}' INTO TABLE {table_name} FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n'")
        print("Done")
    except mariadb.Error as error:
        print(f"Error: {error}")

    connexion.commit()
    cursor.closed

if __name__ == "__main__" :
    
    credentials = gettingCredentials()
    connexion = connectToDatabase(credentials)
    
    cursor = connexion.cursor()
    
    listingDatabase(cursor)
    createDatabase(cursor, "point_of_interest")
    useWorkplace(cursor, "point_of_interest")
    
    createTable(connexion, "allCountries")
    importData(cursor, "./Data/Raw/allCountries/allCountries.txt", "allCountries")
    
    cursor.execute("SELECT * FROM allCountries LIMIT 10")
    results = cursor.fetchall()
    
    for i in results:
        print(i)
    
    cursor.close()
    connexion.close()
    
    # elasticsearch : indexation surtout textuelle (browser like)
    # Spark gérer facilement des cluster de données facilement 
    # Tester des If truc OR machin pour les switch avec argparse (cf. init_all ou just import on mariaDB)
    # check : https://datahub.io/core/geo-countries on pourrait créer une base de données pour ça et essayer d'afficher le lieu avec 
    # les coordonnées GPS