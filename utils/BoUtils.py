from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from utils.table_utils import validate_schema
from utils.BaseClassUtils import BaseClassUtils
from datetime import datetime

import resources.cli_styles as cs

class BoUtils( BaseClassUtils ):

	def __init__(self, objName, toFile = False):
		'''We need to validate that this is a legit object in the json schema.'''
		super(BoUtils, self).__init__('BoUtils')
		self.objName = objName
		self.v_objName = self.uncapitalize(objName)
		self.dbSchema = self.getSchema(objName)
		self.objSchema = self.dbSchema[objName]
		self.type = "bo"
		self.toFile = toFile

	def generateClass(self):
		self.openFile()

		self.generateCommentBlock()
		self.generateImports()
		self.generateClassSignature()
		self.generateInit()
		self.generateGettersAndSetters()
		self.generateObjectGettersForFK()
		self.generateCrudFunctions()
		self.generateRefObjects()
		self.generateToJson()

		self.closeFile()

	def generateCommentBlock(self):
		"""Creates a comment block about the class."""
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#  WARNING: This is an auto-generated file. Do not modify this file.", cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#", cs.PASTEL_YELLOW)
		self.printt_cls("#   {}BO Class".format(self.objName), cs.PASTEL_YELLOW)
		self.printt_cls("#", cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#  Generated on: {ts}".format(ts = str(datetime.now())), cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)

	def generateImports(self):
		"""Creates import statemnts for referencd objects."""
		self.printt_cls("from app.bo.Base import BaseBO")
		self.printt_cls("from app.do.{} import {}DO".format(self.objName, self.objName))
		self.printt_cls("")
		self.printt_cls("from app.dao.{} import {}DAO".format(self.objName, self.v_objName))
		for obj in self.dbSchema.keys():
			if obj == self.objName:
				for field in self.dbSchema[obj]["fields"]:
					if "references" in field:
						ref_table = field["references"]["ref_table"]
						self.printt_cls("from app.dao.{} import {}DAO".format(ref_table, self.uncapitalize(ref_table)))
						self.printt_cls("from app.do.{} import {}DO".format(ref_table, ref_table))
			else:
				for field in self.dbSchema[obj]["fields"]:
					if "references" in field and field["references"]["ref_table"] == self.objName:
						self.printt_cls("from app.dao.{} import {}DAO".format(obj, self.uncapitalize(obj)))
		self.printt_cls("")
		self.printt_cls("")

	def generateClassSignature(self):
		"""Creates class signature."""
		self.printt_cls("class {}BO( BaseBO ):".format(self.objName))
		self.printt_cls("\t'''Used for representing a business object {}.'''".format(self.v_objName))
		self.printt_cls("")

	def generateInit(self):
		"""Creates the init function. Must accept a valid DO object."""
		self.printt_cls("\tdef __init__(self, {} = None):".format(self.v_objName))
		self.printt_cls("\t\t'''Must accept a valid {}DO object.'''".format(self.objName))
		self.printt_cls("\t\tsuper({}BO, self).__init__('{}BO')".format(self.objName, self.objName))
		self.printt_cls("\t\tself.{} = {} if {} else {}DO()".format(self.v_objName, self.v_objName, self.v_objName, self.objName))
		for col in self.objSchema["fields"]:
			col_name = col["name"]
			if "references" in col:
				ref_table = col["references"]["ref_table"]
				u_ref_table = self.uncapitalize(ref_table)
				self.printt_cls("\t\tself.{} = {}DAO.get{}ById({}.{}) if {} else {}DO()".format(u_ref_table, u_ref_table, ref_table, self.v_objName, col_name, self.v_objName, ref_table))
		self.printt_cls("")

	def generateGettersAndSetters(self):
		#TODO: We need to handle reference columns col["references"]
		"""Creates getters and setters for every field of the object."""
		self.printt_cls("\t# ==================================")
		self.printt_cls("\t#  Property Functions")
		self.printt_cls("\t# ==================================")
		for col in self.objSchema["fields"]:
			col_name = col["name"]
			u_col_name = self.uncapitalize(col_name)
			if col_name == "Id":
				self.printt_cls("\tdef get{}(self):".format(col_name))
				self.printt_cls("\t\treturn self.{}.{}".format(self.v_objName, col_name))
				self.printt_cls("")
				continue
			# elif "references" not in col:
			else:
				self.printt_cls("\tdef get{}(self):".format(col_name))
				self.printt_cls("\t\treturn self.{}.{}".format(self.v_objName, col_name))
				self.printt_cls("")
				self.printt_cls("\tdef set{}(self, {}):".format(col_name, u_col_name))
				self.printt_cls("\t\tself.{}.{} = {}".format(self.v_objName, col_name, u_col_name))
				self.printt_cls("")

	def generateObjectGettersForFK(self):
		self.printt_cls("\t# ==================================")
		self.printt_cls("\t#  Foreign Key Functions")
		self.printt_cls("\t# ==================================")
		for col in self.objSchema["fields"]:
			# col_name = col["name"]
			if "references" in col:
				ref_table = col["references"]["ref_table"]
				u_ref_table = self.uncapitalize(ref_table)
				#ref_column = col["references"]["ref_column"]
				self.printt_cls("\tdef get{}(self):".format(ref_table))
				self.printt_cls("\t\tself.{} = {}DAO.get{}ById(self.{}.{})".format(u_ref_table, u_ref_table, ref_table, self.v_objName, col["name"]))
				self.printt_cls("\t\treturn self.{}".format(u_ref_table))
				self.printt_cls("")
				# self.printt_cls("\tdef set{}(self, {}):".format(ref_table, u_ref_table))
				# self.printt_cls("\t\t'''Accepts a DO and stores DO object.'''")
				# self.printt_cls("\t\tself.{}.{} = {}.{}".format(self.v_objName, col_name, u_ref_table, ref_column))
				# self.printt_cls("\t\tself.{} = {}DAO.get{}ById({}.Id)".format(u_ref_table, u_ref_table, ref_table, u_ref_table))
				# self.printt_cls("\t\treturn self.{}".format(u_ref_table))
				# self.printt_cls("")

	def generateCrudFunctions(self):
		"""Creates CRUD functions for the object."""
		self.printt_cls("\t# ==================================")
		self.printt_cls("\t#  CRUD Functions")
		self.printt_cls("\t# ==================================")
		self.printt_cls("\tdef save(self):")
		self.printt_cls("\t\tself.{} = {}DAO.insert{}(self.{})".format(self.v_objName, self.v_objName, self.objName, self.v_objName))
		self.printt_cls("\t\treturn self.{}".format(self.v_objName))
		self.printt_cls("")
		self.printt_cls("\tdef update(self):")
		self.printt_cls("\t\tself.{} = {}DAO.update{}(self.{})".format(self.v_objName, self.v_objName, self.objName, self.v_objName))
		self.printt_cls("\t\treturn self.{}".format(self.v_objName))
		self.printt_cls("")
		self.printt_cls("\tdef delete(self):")
		self.printt_cls("\t\treturn {}DAO.deleteBy{}(self.{})".format(self.v_objName, self.objName, self.v_objName))
		self.printt_cls("")

	def generateRefObjects(self):
		"""Creates a method that list all objects that FK to this object."""
		for obj in self.dbSchema.keys():
			if obj == self.objName:
				continue
			for field in self.dbSchema[obj]["fields"]:
				if "references" in field and field["references"]["ref_table"] == self.objName:
					u_obj = self.uncapitalize(obj)
					u_col_name = field["name"]
					self.printt_cls("\t# ==================================")
					self.printt_cls("\t#  {} List Functions".format(obj))
					self.printt_cls("\t# ==================================")
					self.printt_cls("\tdef get{}s(self):".format(obj))
					self.printt_cls("\t\t'''Returns {}s belonging to this {}.'''".format(u_obj, self.v_objName))
					self.printt_cls("\t\tself.{}s = {}DAO.get{}sFor{}(self.{})".format(u_obj, u_obj, obj, self.objName, self.v_objName))
					self.printt_cls("\t\treturn self.{}s".format(u_obj))
					self.printt_cls("")
					self.printt_cls("\tdef add{}(self, {}):".format(obj, u_obj))
					self.printt_cls("\t\t{}.{} = self.{}.Id".format(u_obj, u_col_name, self.v_objName))
					self.printt_cls("\t\t{} = {}DAO.update{}({})".format(u_obj, u_obj, obj, u_obj))
					self.printt_cls("\t\tself.{}s.append({})".format(u_obj, u_obj))
					self.printt_cls("")
					self.printt_cls("\tdef remove{}(self, {}):".format(obj, u_obj))
					self.printt_cls("\t\t'''TODO: This method can probably be removed.'''")
					self.printt_cls("\t\tself.{}s = self.{}s.remove({})".format(u_obj, u_obj, u_obj))
					self.printt_cls("\t\t{}DAO.deleteBy{}({})".format(u_obj, obj, u_obj))
					self.printt_cls("")

	def generateToJson(self):
		'''Generates a method that will return a JSON representation of BO.'''
		self.printt_cls("\tdef toJson(self):")
		self.printt_cls("\t\t'''Returns a JSON representation of BO.'''")
		self.printt_cls("\t\tboJson = self.{}.toJson()".format(self.v_objName))

		# Get the FK object.
		for col in self.objSchema["fields"]:
			if "references" in col:
				ref_table = col["references"]["ref_table"]
				u_ref_table = self.uncapitalize(ref_table)
				self.printt_cls("\t\tboJson['{}'] = self.{}.toJson()".format(ref_table, u_ref_table))
		self.printt_cls("")
		
		# Get objects referencing.
		for obj in self.dbSchema.keys():
			if obj == self.objName:
				continue
			for field in self.dbSchema[obj]["fields"]:
				if "references" in field and field["references"]["ref_table"] == self.objName:
					u_obj = self.uncapitalize(obj)
					self.printt_cls("\t\tself.{}s = {}DAO.get{}sFor{}(self.{})".format(u_obj, u_obj, obj, self.objName, self.v_objName))
					self.printt_cls("\t\tboJson['{}List'] = [c.toJson() for c in self.{}s]".format(u_obj, u_obj))
					self.printt_cls("")
		self.printt_cls("\t\treturn boJson")