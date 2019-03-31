from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.properties_utils import get_db_properties

from mysql.connector import errorcode, connection

class DatabaseConnection(object):
	'''Singleton class for a MySQL connection'''
	instance = None
	connection = None # Stores a single db connection that would be used through the app.

	def __new__(cls):
		if DatabaseConnection.instance is None:
			DatabaseConnection.instance = object.__new__(cls)
		return DatabaseConnection.instance

	def __init__(self):
		'''Creates and opens a single db connection.'''
		if DatabaseConnection.connection is None:
			db_config = get_db_properties()
			try:
				DatabaseConnection.connection = connection.MySQLConnection(
					user = db_config["dbUsername"],
					password = db_config["dbPassword"],
					host = db_config["dbHost"],
					database = db_config["dbName"])
				DatabaseConnection.connection.autocommit = True
			except mysql.connector.Error as err:

				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					printt_error("Invalid username or password.")
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					printt_error("Database does not exist.")
				else:
					printt_error(str(err))
				return

	def __del__(self):
		'''Closes the database connection.'''
		if DatabaseConnection.connection:
			DatabaseConnection.connection.close()

	def execute_query(self, query = None, data = None):
		'''Executes the insert/update sql query.'''
		if DatabaseConnection.connection is None:
			printt_error("Database connection is null.")
		cursor = DatabaseConnection.connection.cursor()
		cursor.execute(query, data)
		rowsAffected = cursor.rowcount
		DatabaseConnection.connection.commit()
		cursor.close()
		return rowsAffected

	def insert_one(self, query = None, data = None):
		'''Executes the insert/update sql query.'''
		if DatabaseConnection.connection is None:
			printt_error("Database connection is null.")
		cursor = DatabaseConnection.connection.cursor()
		cursor.execute(query, data)
		row_id = cursor.lastrowid
		DatabaseConnection.connection.commit()
		cursor.close()
		return row_id

	def update_one(self, query = None, data = None):
		'''Executes the insert/update sql query.'''
		if DatabaseConnection.connection is None:
			printt_error("Database connection is null.")
		cursor = DatabaseConnection.connection.cursor()
		cursor.execute(query, data)
		row_id = cursor.lastrowid
		DatabaseConnection.connection.commit()
		cursor.close()
		return row_id

	def query_single_result(self, query = None, data = None):
		'''Executes the sql query and returns a single row of data.'''
		if DatabaseConnection.connection is None:
			printt_error("Database connection is null.")
		cursor = DatabaseConnection.connection.cursor(dictionary = True)
		cursor.execute(query, data)
		row = cursor.fetchone()
		cursor.close()
		return row

	def query_many_result(self, query = None, count = 1, data = None):
		'''Executes the sql query and returns a max number of result (for pagination).'''
		if DatabaseConnection.connection is None:
			printt_error("Database connection is null.")
		cursor = DatabaseConnection.connection.cursor(dictionary = True)
		cursor.execute(query, data)
		resultSet = cursor.fetchmany(count)
		cursor.close()
		return resultSet

	def query_all_result(self, query = None, data = None):
		'''Executes the sql query and returns all the results of the table.'''
		if DatabaseConnection.connection is None:
			printt_error("Database connection is null.")
		cursor = DatabaseConnection.connection.cursor(dictionary = True)
		cursor.execute(query, data)
		resultSet = cursor.fetchall()
		cursor.close()
		return resultSet

	def count_entries(self, table_name):
		query = "SELECT COUNT(*) FROM {}".format(table_name)
		if DatabaseConnection.connection is None:
			printt_error("Database connection is null.")
		cursor = DatabaseConnection.connection.cursor()
		cursor.execute(query)
		resultSet = cursor.fetchall()
		rowCount = cursor.rowcount
		cursor.close()
		return rowCount

	def query_table_exists(self, table_name):
		'''Determines if table exists.'''
		if not table_name:
			return False
		query = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{}'".format(table_name)
		cursor = DatabaseConnection.connection.cursor()
		cursor.execute(query)
		result = cursor.fetchone()
		if result[0] == 1:
			cursor.close()
			return True
		cursor.close()
		return False
