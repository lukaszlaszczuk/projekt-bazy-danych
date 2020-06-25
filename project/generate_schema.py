import logging
import os
import sys


from util.MySQLConnector import MySQLConnector

if len(sys.argv) < 4:
    raise Exception("You have to specify hostname, user and password to Your database")

host, user, password = sys.argv[1:]
logging.getLogger().setLevel(logging.INFO)
logging.info(f'host: {host}, user: {user}, password: {password}')
sql_script_path = os.path.join('sqls', 'sql_create_database.sql')

db_connection = MySQLConnector.connect(host, user, password)
cursor = MySQLConnector.get_cursor(db_connection)
MySQLConnector.execute_script(cursor, sql_script_path)
MySQLConnector.close_connection(db_connection)
logging.info('Generowanie schematu bazy danych ukończone!')
