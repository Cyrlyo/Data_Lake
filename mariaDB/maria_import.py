import mariadb
import pandas as pd
import os
from mariadb.cursors import Cursor
from utils_db import gettingCredentials, connectToDatabase, listingDatabase, \
    createDatabase, dropDatabase, useWorkplace

def createTable(cursor: Cursor):
    
    cursor.execute("DROP TABLE IF EXISTS test")
    createtable_query = "CREATE TABLE test(geonameid INT, name VARCHAR(255), asciiname VARCHAR(255), alternatenames VARCHAR(255), latitude FLOAT, longitude FLOAT, feature_class VARCHAR(255), feature_code VARCHAR(255), country_code VARCHAR(255), cc2 VARCHAR(255), admin1_code VARCHAR(255), admin2_code VARCHAR(255), admin3_code VARCHAR(255), admin4_code VARCHAR(255), population INT, elevation FLOAT, dem INT, timezone VARCHAR(255), modification_date DATE)"
    
    try:
        cursor.execute(createtable_query)
    except mariadb.Error as error:
        print(f"Error: {error}")
    
    try:
        path = os.getcwd()
        print(path)
        data_path = os.path.join(path, "Data/Raw/allCountries/allCountries.csv")
        print(data_path)
        data_path = "C:/Users/Marin/Desktop/Cours/M2/S1/Data Lake & Analytics/Projet/Scripts/Data/Raw/allCountries/allCountries.txt"
        cursor.execute(f"LOAD DATA LOCAL INFILE '{data_path}' INTO TABLE test FIELDS TERMINATED BY '\t'")
    except mariadb.Error as error:
        print(f"Error: {error}")


if __name__ == "__main__" :
    
    credentials = gettingCredentials()
    connexion = connectToDatabase(credentials)
    
    cursor = connexion.cursor()
    
    listingDatabase(cursor)
    # createDatabase(cursor, "python_created_test")
    useWorkplace(cursor, "python_created_test")

    createTable(cursor)
    
    names = ["geonameid","name","asciiname","alternatenames","latitude","longitude","feature class","feature code","country code","cc2","admin1 code","admin2 code","admin3 code","admin4 code","population","elevation","dem","timezone","modification date"]

    cursor.execute("SELECT * FROM test LIMIT 10")
    results = cursor.fetchall()
    
    for i in results:
        print(i)

    # data = pd.read_csv("./Data/Raw/allCountries/allCountries.txt", sep="\t", header=None, names=names)
    
    # dropDatabase(cursor, "python_created_test")
    
    # elasticsearch : indexation surtout textuelle (browser like)
    # Spark gérer facilement des cluster de données facilement 