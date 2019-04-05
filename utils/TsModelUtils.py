from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from utils.table_utils import validate_schema
from utils.BaseClassUtils import BaseClassUtils
from datetime import datetime

import resources.cli_styles as cs

class TsModelUtils( BaseClassUtils ):

	JS_DATA_TYPES = {
		"bool" : 		"boolean",
		"date" : 		"string",
		"double" :		"number",
		"int" : 		"number",
		"str" :			"string",
		"text" :		"string",
		"timestamp" :	"string"
	}

	def __init__(self, objName, toFile = False):
		'''We need to validate that this is a legit object in the json schema.'''
		super(TsModelUtils, self).__init__('TsModelUtils')
		self.objName = objName
		self.uObjName = self.uncapitalize(objName)
		self.dbSchema = self.getSchema(objName)
		self.objSchema = self.dbSchema[objName]
		self.toFile = toFile
		self.fullFilePath = "../../NodeServer/appServer/src/app/{}.ts".format(self.uObjName)

	def generateClass(self):
		self.openFile()

		#self.generateCommentBlock()
		self.generateModelClass()

		self.closeFile()

	def generateCommentBlock(self):
		"""Creates a comment block about the class."""
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#  WARNING: This is an auto-generated file. Do not modify this file.", cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#", cs.PASTEL_YELLOW)
		self.printt_cls("#   {} Model".format(self.objName), cs.PASTEL_YELLOW)
		self.printt_cls("#", cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#  Generated on: {ts}".format(ts = str(datetime.now())), cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)

	def generateModelClass(self):
		"""Creates endpoints for get all BO objects."""
		self.printt_cls("export class {} {}".format(self.objName, "{"))
		for col in self.objSchema["fields"]:
			colName = col["name"]
			colType = col["type"]
			self.printt_cls("\t{} : {};".format(colName, self.JS_DATA_TYPES[colType]))
		self.printt_cls("}")
		self.printt_cls("")
