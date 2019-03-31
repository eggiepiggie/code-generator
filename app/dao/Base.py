from utils.DatabaseConnection import DatabaseConnection

class BaseDAO(object):
	'''Parent Base DO class.'''
	dbConnection = None

	def __init__(self, class_name = "BaseDAO"):
		self.class_name = class_name
		self.dbConnection = DatabaseConnection()
