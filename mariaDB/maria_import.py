import mariadb
import yaml


print("coucou0")
connexion = mariadb.connect(
    user = "root",
    password = "root",
    host = "localhost",
    port = 3306
)
print("coucou1")
print(connexion)

print("coucou3")
cursor = connexion.cursor()
print("coucour4")
print(cursor)

print("coucou5")
cursor.execute("SHOW DATABASES")
print("coucou6")

data_base_list = cursor.fetchall()
  
for database in data_base_list:
  print(database)