from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from utils.table_utils import validate_schema
from datetime import datetime

import resources.cli_styles as cs


class BaseClassUtils(object):

	def __init__(self, class_name = "BaseDAO"):
		self.class_name = class_name

	def openFile(self):
		'''Opens the file for write access.'''
		if self.toFile:
			self.boFile = open('app/{}/{}.py'.format(self.type, self.objName), 'w')

	def closeFile(self):
		'''Closes the file.'''
		if self.toFile:
			self.boFile.close()

	def printt_cls(self, text = "", colour = cs.DEFAULT):
		if self.toFile:
			printt(text, colour, self.boFile)
		else:
			printt(text, colour)

	def getSchema(self, objName):
		dbSchema = load_json("resources/database-structure-definition.json")
		if not validate_schema(dbSchema, objName):
			raise Exception('The object name provided does not exists.')
		return dbSchema

	def uncapitalize(self, text):
		'''Lowercases the first letter of the text.'''
		return text[:1].lower() + text[1:]

	def isUnique(self, column):
		'''Returns true if column holds unique values'''
		return (("is_unique" in column and column["is_unique"])
					or ("auto_inc" in column and column["auto_inc"])
					or ("is_pk" in column and column["is_pk"]))

	def getEscCharacters(self, column):
		col_type = column["type"]
		if col_type == "bool" or col_type == "int" or col_type == "double":
			return "{}"
		else:
			return "'{}'"