import mariadb
import pandas as pd
import os
from mariadb.cursors import Cursor
from mariadb.connections import Connection
from utils_db import gettingCredentials, connectToDatabase, listingDatabase, \
    createDatabase, dropDatabase, useWorkplace

def createTable(connexion: Connection):
    
    cursor = connexion.cursor()
    cursor.execute("DROP TABLE IF EXISTS test")
    #TODO: Do a F-string and add table_name as argument and print(importing data)
    createtable_query = "CREATE TABLE test(geonameid BIGINT NOT NULL UNIQUE, name VARCHAR(200) COLLATE utf8_general_ci, asciiname VARCHAR(200), alternatenames VARCHAR(10000), latitude FLOAT, longitude FLOAT, feature_class CHAR(1), feature_code VARCHAR(10), country_code VARCHAR(255), cc2 VARCHAR(255), admin1_code VARCHAR(20), admin2_code VARCHAR(80), admin3_code VARCHAR(20), admin4_code VARCHAR(20), population BIGINT, elevation FLOAT, dem INT, timezone VARCHAR(40), modification_date DATE, PRIMARY KEY (geonameid))"
    
    try:
        cursor.execute(createtable_query)
    except mariadb.Error as error:
        print(f"Error: {error}")

def importData(cursor: Cursor):
    try:
        #TODO: faire fonction pour path correct
        path = os.getcwd()
        # data_path = os.path.join(path, "Data/Raw/allCountries/allCountries.csv")
        # print(data_path)
        print("\nImporting data... Please wait")
        data_path = "C:/Users/Marin/Desktop/Cours/M2/S1/Data Lake & Analytics/Projet/Scripts/Data/Raw/allCountries/allCountries.txt"
        cursor.execute(f"LOAD DATA LOCAL INFILE '{data_path}' INTO TABLE test FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n'")
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
    createDatabase(cursor, "python_created_test")
    useWorkplace(cursor, "python_created_test")
    
    createTable(connexion)
    importData(cursor)
    
    cursor.execute("SELECT * FROM test LIMIT 10")
    results = cursor.fetchall()
    
    # for i in results:
        # print(i)

    # data = pd.read_csv("./Data/Raw/allCountries/allCountries.txt", sep="\t", header=None, names=names)
    
    # dropDatabase(cursor, "python_created_test")
    
    # elasticsearch : indexation surtout textuelle (browser like)
    # Spark gérer facilement des cluster de données facilement 