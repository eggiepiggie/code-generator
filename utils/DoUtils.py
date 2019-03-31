from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from utils.table_utils import validate_schema
from utils.BaseClassUtils import BaseClassUtils
from datetime import datetime

import resources.cli_styles as cs

class DoUtils( BaseClassUtils ):

	def __init__(self, objName, toFile = False):
		super(DoUtils, self).__init__('DoUtils')
		self.objName = objName
		self.v_objName = self.uncapitalize(objName)
		self.dbSchema = self.getSchema(objName)
		self.objSchema = self.dbSchema[objName]
		self.type = "do"
		self.toFile = toFile

	def generateClass(self):

		self.openFile()

		self.generateCommentBlock()
		self.generateClassSignature()
		self.generateInit()
		self.generateToJson()
		self.generateToString()
		self.generateEqualsTo()
		self.generateToObj()

		self.closeFile()

	def generateCommentBlock(self):
		"""Creates a comment block about the class."""
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#  WARNING: This is an auto-generated file. Do not modify this file.", cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#", cs.PASTEL_YELLOW)
		self.printt_cls("#   {}DO Class".format(self.objName), cs.PASTEL_YELLOW)
		self.printt_cls("#", cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#  Generated on: {ts}".format(ts = str(datetime.now())), cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)

	def generateClassSignature(self):
		"""Creates base import statement and class signature."""
		self.printt_cls("from app.do.Base import BaseDO")
		self.printt_cls("")
		self.printt_cls("")
		self.printt_cls("class {}DO( BaseDO ):".format(self.objName))

	def generateInit(self):
		"""Creates constructor method for given object."""
		init_params = "self"
		for col in self.objSchema["fields"]:
			init_params += ", {} = None".format(self.uncapitalize(col["name"]))

		self.printt_cls("\tdef __init__({}):".format(init_params))
		for col in self.objSchema["fields"]:
			name = col["name"]
			self.printt_cls("\t\tself.{} = {}".format(name, self.uncapitalize(name)))
		self.printt_cls("")

	def generateToJson(self):
		'''Generates a method for converting object to json for serialization.'''
		self.printt_cls("\tdef toJson(self, simple = False):")
		self.printt_cls("\t\t'''Converts this object into a json.'''")
		self.printt_cls("\t\tobjJson = {}")
		self.printt_cls("\t\tif simple:")
		self.printt_cls("\t\t\tobjJson['Id'] = self.Id")
		self.printt_cls("\t\telse:")
		for col in self.objSchema["fields"]:
			if (col["type"] == "date"):
				self.printt_cls("\t\t\tobjJson['{}'] = str(self.{})".format(col["name"], col["name"]))
			else:
				self.printt_cls("\t\t\tobjJson['{}'] = self.{}".format(col["name"], col["name"]))
		self.printt_cls("\t\treturn objJson")
		self.printt_cls("")

	def generateToString(self):
		'''Generates a method for creating string representation of objects.'''
		self.printt_cls("\tdef toString(self):")
		self.printt_cls("\t\t'''Generates a string representation of this object.'''")
		params = []
		data = []
		for col in self.objSchema["fields"]:
			col_name = col["name"]
			u_col_name = self.uncapitalize(col_name)
			params.append("{}={}".format(u_col_name, "{}"))
			data.append("self.{}".format(col_name))
		params = ", ".join(params)
		data = ", ".join(data)
		self.printt_cls("\t\treturn \"{}DO[{}]\".format({})".format(self.objName, params, data))
		self.printt_cls("")

	def generateEqualsTo(self):
		'''Generates a method for comparing one object to another object.'''
		self.printt_cls("\tdef equalsTo(self, {}):".format(self.v_objName))
		self.printt_cls("\t\t'''Compares this object with another object to see if they are equal.'''")
		for col in self.objSchema["fields"]:
			col_name = col["name"]
			if col_name == "Id":
				continue
			self.printt_cls("\t\tif self.{} != {}.{}:".format(col_name, self.v_objName, col_name))
			self.printt_cls("\t\t\treturn False")
		self.printt_cls("\t\treturn True")
		self.printt_cls("")

	def generateToObj(self):
		'''Generates a method for converting a json into specified object.'''
		self.printt_cls("\t@classmethod")
		self.printt_cls("\tdef toObj(self, objJson = {}):")
		self.printt_cls("\t\t'''Converts json into a object.'''")
		self.printt_cls("\t\t{} = {}DO()".format(self.v_objName, self.objName))
		for col in self.objSchema["fields"]:
			self.printt_cls("\t\t{}.{} = objJson['{}'] if '{}' in objJson else None".format(self.v_objName, col["name"], col["name"], col["name"]))
		self.printt_cls("\t\treturn {}".format(self.v_objName))
		self.printt_cls("")
