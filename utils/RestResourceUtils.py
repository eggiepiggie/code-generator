from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from utils.table_utils import validate_schema
from utils.BaseClassUtils import BaseClassUtils
from datetime import datetime

import resources.cli_styles as cs

class RestApiEggieUtils( BaseClassUtils ):

	def __init__(self, objName, toFile = False):
		'''We need to validate that this is a legit object in the json schema.'''
		super(RestApiEggieUtils, self).__init__('RestApiEggieUtils')
		self.objName = objName
		self.v_objName = self.uncapitalize(objName)
		self.dbSchema = self.getSchema(objName)
		self.objSchema = self.dbSchema[objName]
		self.type = "rest_api"
		self.toFile = toFile

	def generateClass(self):
		file = open('app/rest_api/MarketResources.py'.format(self.type, self.objName), 'w')

		self.generateCommentBlock()
		self.generateImports()
		self.generateGetAll()
		self.generateById()
		self.generateReference()
		self.generateRequestParameterParser()

		file.close()
