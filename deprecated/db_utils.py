from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.properties_utils import get_db_properties

import mysql.connector
from mysql.connector import errorcode, connection

class DatabaseConnection:
	'''Singleton class for a MySQL connection'''
	__instance = None
	__connection = None # Stores a single db connection that would be used through the app.

	def __new__(cls):
		if DatabaseConnection.__instance is None:
			DatabaseConnection.__instance = object.__new__(cls)
		return DatabaseConnection.__instance

	def __init__(self):
		'''Creates and opens a single db connection.'''
		if DatabaseConnection.__connection is None:
			db_config = get_db_properties()
			try:
				DatabaseConnection.__connection = connection.MySQLConnection(
					user = db_config["dbUsername"],
					password = db_config["dbPassword"],
					host = db_config["dbHost"],
					database = db_config["dbName"])
			except mysql.connector.Error as err:

				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					printt_error("Invalid username or password.")
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					printt_error("Database does not exist.")
				else:
					printt_error(err)
				return
		return DatabaseConnection.__connection

	def __del__(self):
		'''Closes the database connection.'''
		if DatabaseConnection.__connection:
			DatabaseConnection.__connection.close()

	def execute_query(self, query = None, data = None):
		'''Executes the insert/update sql query.'''
		if DatabaseConnection.__connection is None:
			printt_error("Database connection is null.")
		cursor = DatabaseConnection.__connection.cursor()
		cursor.execute(query, data)
		DatabaseConnection.__connection.commit()
		cursor.close()

	def query_single_result(self, query = None, data = None):
		'''Executes the sql query and returns a single row of data.'''
		if DatabaseConnection.__connection is None:
			printt_error("Database connection is null.")
		cursor = DatabaseConnection.__connection.cursor()
		cursor.execute(query, data)
		row = cursor.fetchone()
		cursor.close()
		return row

	def query_many_result(self, query = None, count = 1, data = None):
		'''Executes the sql query and returns a max number of result (for pagination).'''
		if DatabaseConnection.__connection is None:
			printt_error("Database connection is null.")
		cursor = DatabaseConnection.__connection.cursor()
		cursor.execute(query, data)
		resultSet = cursor.fetchmany(count)
		cursor.close()
		return resultSet

	def query_all_result(self, query = None, data = None):
		'''Executes the sql query and returns all the results of the table.'''
		if DatabaseConnection.__connection is None:
			printt_error("Database connection is null.")
		cursor = DatabaseConnection.__connection.cursor()
		cursor.execute(query, data)
		resultSet = cursor.fetchall()
		cursor.close()
		return resultSet

