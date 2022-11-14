import mariadb
from utils_db import gettingCredentials, connectToDatabase, listingDatabase, \
    createDatabase, dropDatabase, useWorkplace



if __name__ == "__main__" :
    
    credentials = gettingCredentials()
    connexion = connectToDatabase(credentials)
    
    cursor = connexion.cursor()
    
    listingDatabase(cursor)
    createDatabase(cursor, "python_created_test")
    useWorkplace(cursor, "python_created_test")
    
    # dropDatabase(cursor, "python_created_test")