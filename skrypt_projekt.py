import mysql.connector

############################
#     POLACZENIE DO MYSQL  #
############################
mydb = mysql.connector.connect(
  host="localhost",
  user="root"
)
mycursor = mydb.cursor()

############################
#      WCZYTANIE SKRYPTU   #             
############################

with open('sql_create_database.sql') as sql_script:
    script = sql_script.read().replace('\n', '')
    
############################
#   PUSZCZENIE SKRYPTU     #
############################

mycursor.execute(script)
mydb.close()

