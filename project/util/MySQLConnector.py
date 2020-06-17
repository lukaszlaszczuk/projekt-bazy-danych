import logging
import mysql.connector


class MySQLConnector:

    @staticmethod
    def connect(host, user, password=None, database=''):
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        logging.info(f'Succesfully connected to {host}!')
        return connection

    @staticmethod
    def get_cursor(connection):
        cursor = connection.cursor()
        logging.info(f'Cursor created')
        return cursor

    @staticmethod
    def execute_script(cursor, filename, multi=False):
        with open(filename) as sql_script:
            script = sql_script.read().replace('\n', '')
        cursor.execute(script, multi=multi)

    @staticmethod
    def executemany(cursor, query, table):
        cursor.executemany(query, table)
        return

    @staticmethod
    def commit(connection):
        connection.commit()

    @staticmethod
    def close_connection(connection):
        connection.close()
        logging.info('Database connection closed.')
