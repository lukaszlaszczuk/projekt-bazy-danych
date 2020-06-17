import logging
import os


from util.MySQLConnector import MySQLConnector

logging.getLogger().setLevel(logging.INFO)
sql_script_path = os.path.join('sqls', 'sql_create_database.sql')

db_connection = MySQLConnector.connect('localhost', 'root')
cursor = MySQLConnector.get_cursor(db_connection)
MySQLConnector.execute_script(cursor, sql_script_path)
MySQLConnector.close_connection(db_connection)
logging.info('Generowanie schematu bazy danych ukończone!')
