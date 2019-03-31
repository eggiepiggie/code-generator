from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from utils.table_utils import validate_schema
from utils.BaseClassUtils import BaseClassUtils
from datetime import datetime

import resources.cli_styles as cs

class DaoUtils( BaseClassUtils ):

	def __init__(self, objName, toFile = False):
		super(DaoUtils, self).__init__('DaoUtils')
		self.objName = objName
		self.v_objName = self.uncapitalize(objName)
		self.dbSchema = self.getSchema(objName)
		self.objSchema = self.dbSchema[objName]
		self.type = "dao"
		self.toFile = toFile

	def generateClass(self):

		self.openFile()

		self.generateCommentBlock()
		self.generateClassSignature()
		self.generateInit()
		self.generateInsert()
		self.generateUpdate()
		self.generateDeleteMethods()
		self.generateGetAll()
		self.generateSelectByKey()
		self.generateSelectForOtherObjects()
		self.generateInstance()

		self.closeFile()

	def generateCommentBlock(self):
		"""Creates a comment block about the class."""
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#  WARNING: This is an auto-generated file. Do not modify this file.", cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#", cs.PASTEL_YELLOW)
		self.printt_cls("#   {}DAO Class".format(self.objName), cs.PASTEL_YELLOW)
		self.printt_cls("#", cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#  Generated on: {ts}".format(ts = str(datetime.now())), cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)

	def generateClassSignature(self):
		self.printt_cls("from app.dao.Base import BaseDAO")
		self.printt_cls("from app.do.{} import {}DO".format(self.objName, self.objName))
		#self.printt_cls("import app.do.{}".format(self.objName))
		self.printt_cls("")
		self.printt_cls("")
		self.printt_cls("class {}DAO( BaseDAO ):".format(self.objName))
		self.printt_cls("\t'''Used for accessing datastore for {} objects.'''".format(self.objName))
		self.printt_cls("")

	def generateInit(self):
		self.printt_cls("\tdef __init__(self):")
		self.printt_cls("\t\tsuper({}DAO, self).__init__('{}DAO')".format(self.objName, self.objName))
		self.printt_cls("")

	def generateInsert(self):
		self.printt_cls("\tdef insert{}(self, {} = None):".format(self.objName, self.v_objName))
		self.printt_cls("\t\t'''Persists {} to the database.'''".format(self.v_objName))
		self.printt_cls("\t\tif not {}:".format(self.v_objName))
		self.printt_cls("\t\t\treturn")
		self.printt_cls("")
		self.buildInsertSql()
		self.printt_cls("\t\t{}.Id = self.dbConnection.instance.insert_one(insertSql, insertData)".format(self.v_objName))
		self.printt_cls("\t\treturn {}".format(self.v_objName))
		self.printt_cls("")

	def generateUpdate(self):
		self.printt_cls("\tdef update{}(self, {} = None):".format(self.objName, self.v_objName))
		self.printt_cls("\t\t'''Updates and persists {} to the database.'''".format(self.v_objName))
		self.printt_cls("\t\tif not {}:".format(self.v_objName))
		self.printt_cls("\t\t\treturn")
		self.printt_cls("")
		self.buildUpdateSql()
		self.printt_cls("\t\t{}.Id = self.dbConnection.instance.update_one(updateSql, updateData)".format(self.v_objName))
		self.printt_cls("\t\treturn {}".format(self.v_objName))
		self.printt_cls("")

	def generateDeleteMethods(self):
		for col in self.objSchema["fields"]:
			if self.isUnique(col):
				col_name = col["name"]
				u_col_name = self.uncapitalize(col_name)

				self.printt_cls("\tdef deleteBy{}(self, {} = None):".format(col_name, u_col_name))
				self.printt_cls("\t\t'''Deletes {} object from the database by {}.'''".format(self.v_objName, u_col_name))
				self.printt_cls("\t\tif not {}:".format(u_col_name))
				self.printt_cls("\t\t\treturn")
				self.printt_cls("\t\tdeleteBy{}Sql = \"DELETE FROM {} WHERE {} = {}\".format({})".format(col_name, self.objName, col_name, self.getEscCharacters(col), u_col_name))
				self.printt_cls("\t\treturn self.dbConnection.instance.execute_query(deleteBy{}Sql)".format(col_name))
				self.printt_cls("")

		# Creates delete method by object.
		self.printt_cls("\tdef deleteBy{}(self, {} = None):".format(self.objName, self.v_objName))
		self.printt_cls("\t\t'''Deletes {} to the database.'''".format(self.v_objName))
		self.printt_cls("\t\tif not {}:".format(self.v_objName))
		self.printt_cls("\t\t\treturn")
		self.printt_cls("\t\treturn self.deleteById({}.Id)".format(self.v_objName))
		self.printt_cls("")

	def generateGetAll(self):
		'''Creates a method that would get all the objects given a limit.'''
		self.printt_cls("\tdef getAll{}s(self, limit = None):".format(self.objName))	
		self.printt_cls("\t\t'''Returns all {}s.'''".format(self.v_objName))
		self.printt_cls("\t\tselectSql = \"SELECT * FROM {}\"".format(self.objName))
		self.printt_cls("")
		self.printt_cls("\t\tresultSet = self.dbConnection.instance.query_all_result(selectSql)")
		self.printt_cls("\t\tobjList = []")
		self.printt_cls("\t\tfor row in resultSet:")
		self.printt_cls("\t\t\t{} = {}DO.toObj(row)".format(self.v_objName, self.objName))
		self.printt_cls("\t\t\tobjList.append({})".format(self.v_objName))
		self.printt_cls("\t\treturn objList")
		self.printt_cls("")

	def buildInsertSql(self):
		params = []
		data = []

		for col in self.objSchema["fields"]:
			if col["name"] == "Id":
				continue
			else:
				params.append(col["name"])
				data.append("%({})s".format(self.uncapitalize(col["name"])))

		params = ", ".join(params)
		data = ", ".join(data)

		self.printt_cls("\t\tinsertSql = (\"INSERT INTO {} \"".format(self.objName))
		self.printt_cls("\t\t\t\"({}) \"".format(params))
		self.printt_cls("\t\t\t\"VALUES ({})\")".format(data))
		self.printt_cls("")
		self.printt_cls("\t\tinsertData = {")
		for col in self.objSchema["fields"]:
			col_name = col["name"]
			u_col_name = self.uncapitalize(col_name)
			if col_name == "Id":
				continue
			else:
				self.printt_cls("\t\t\t'{}' : {}.{},".format(u_col_name, self.v_objName, col_name))
		self.printt_cls("\t\t}")
		self.printt_cls("")

	def generateSelectByKey(self):
		"""Creates methods for fetching by unique key (e.g. id, name, etc.)."""
		for col in self.objSchema["fields"]:
			if self.isUnique(col):
				col_name = col["name"]
				u_col_name = self.uncapitalize(col_name)
				self.printt_cls("\tdef get{}By{}(self, {}):".format(self.objName, col_name, u_col_name))
				self.printt_cls("\t\t'''Retrieves {} by {} from the database.'''".format(self.v_objName, u_col_name))
				self.printt_cls("\t\tselectBy{}Sql = \"SELECT * FROM {} WHERE {} = {}\".format({})".format(col_name, self.objName, col_name, self.getEscCharacters(col), u_col_name))
				self.printt_cls("")
				self.printt_cls("\t\tresultSet = self.dbConnection.instance.query_single_result(selectBy{}Sql)".format(col_name))
				self.printt_cls("\t\t{} = {}DO.toObj(resultSet)".format(self.v_objName, self.objName))
				self.printt_cls("\t\treturn {}".format(self.v_objName))
				self.printt_cls("")

	def generateSelectForOtherObjects(self):
		"""Creates a getter for list all object being to a key (foreign key.)"""
		for col in self.objSchema["fields"]:
			if "references" in col:
				col_name = col["name"]
				ref_table = col["references"]["ref_table"]
				u_ref_table = self.uncapitalize(ref_table)
				ref_column = col["references"]["ref_column"]
				self.printt_cls("\tdef get{}sFor{}(self, {}):".format(self.objName, ref_table, u_ref_table))
				self.printt_cls("\t\t'''Returns all the {}s belonging to provided {}.'''".format(self.v_objName, u_ref_table))
				self.printt_cls("\t\tselectSql = \"SELECT * FROM {} WHERE {} = {}\".format({}.{})".format(self.objName, col_name, "{}", u_ref_table, ref_column))
				self.printt_cls("")
				self.printt_cls("\t\tresultSet = self.dbConnection.instance.query_all_result(selectSql)")
				self.printt_cls("\t\tobjList = []")
				self.printt_cls("\t\tfor row in resultSet:")
				self.printt_cls("\t\t\t{} = {}DO.toObj(row)".format(self.v_objName, self.objName))
				self.printt_cls("\t\t\tobjList.append({})".format(self.v_objName))
				self.printt_cls("\t\treturn objList")
				self.printt_cls("")

	def generateInstance(self):
		self.printt_cls("")
		self.printt_cls("{}DAO = {}DAO()".format(self.v_objName, self.objName))

	def buildUpdateSql(self):
		params = []

		for col in self.objSchema["fields"]:
			if col["name"] == "Id":
				continue
			else:
				params.append("{} = %({})s".format(col["name"], self.uncapitalize(col["name"])))

		params = ", ".join(params)

		self.printt_cls("\t\tupdateSql = (\"UPDATE {} \"".format(self.objName))
		self.printt_cls("\t\t\t\"SET {}\"".format(params))
		self.printt_cls("\t\t\t\"WHERE Id = %(id)s\")")
		self.printt_cls("")
		self.printt_cls("\t\tupdateData = {")
		for col in self.objSchema["fields"]:
			col_name = col["name"]
			u_col_name = self.uncapitalize(col_name)
			self.printt_cls("\t\t\t'{}' : {}.{},".format(u_col_name, self.v_objName, col_name))
		self.printt_cls("\t\t}")
		self.printt_cls("")

