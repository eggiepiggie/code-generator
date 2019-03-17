from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.properties_utils import get_db_properties

import mysql.connector
from mysql.connector import errorcode, connection

db_connection = None # Stores a single db connection that would be used through the app.

def connect_db():
	'''Creates and opens a single db connection.'''
	global db_connection
	db_config = get_db_properties()
	try:
		db_connection = connection.MySQLConnection(
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
	return db_connection

def close_db():
	'''Closes the database connection.'''
	global db_connection
	if db_connection:
		db_connection.close()
