from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from utils.table_utils import validate_schema
import utils.db_utils as dbu
from datetime import datetime

import resources.cli_styles as cs

dao_file = None

def initialize(obj_name, to_file = False):
	"""We need to make sure we have the database schema first."""
	db_schema = load_json("resources/database-structure-definition.json")

	if not validate_schema(db_schema, obj_name):
		return 

	if to_file:
		global dao_file
		dao_file = open('app/dao/{}.py'.format(obj_name), 'w')

	create_object_comment_block(obj_name)
	create_class(obj_name)
	create_init_func(obj_name)
	create_insert_object_to_db(obj_name, db_schema[obj_name])
	create_update_object_to_db(obj_name, db_schema[obj_name])
	create_delete_object_to_db(obj_name, db_schema[obj_name])
	create_list_objects_of_type(obj_name)
	create_methods_by_unique_key(obj_name, db_schema[obj_name])
	create_get_objs_for_key(obj_name, db_schema[obj_name])
	printt_dao("")
	printt_dao("{}DAO = {}DAO()".format(uncapitalize(obj_name), obj_name))

	if to_file:
		dao_file.close()

def create_object_comment_block(obj_name):
	"""Creates a comment block about the class."""
	printt_dao("# ===================================================================", cs.PASTEL_YELLOW)
	printt_dao("#  WARNING: This is an auto-generated file. Do not modify this file.", cs.PASTEL_YELLOW)
	printt_dao("# ===================================================================", cs.PASTEL_YELLOW)
	printt_dao("#", cs.PASTEL_YELLOW)
	printt_dao("#   {}DAO Class".format(obj_name), cs.PASTEL_YELLOW)
	printt_dao("#", cs.PASTEL_YELLOW)
	printt_dao("# ===================================================================", cs.PASTEL_YELLOW)
	printt_dao("#  Generated on: {ts}".format(ts = str(datetime.now())), cs.PASTEL_YELLOW)
	printt_dao("# ===================================================================", cs.PASTEL_YELLOW)

def create_class(obj_name):
	printt_dao("from app.dao.Base import BaseDAO")
	printt_dao("from app.bo.{} import {}DO".format(obj_name, obj_name))
	printt_dao("")
	printt_dao("")
	printt_dao("class {}DAO( BaseDAO ):".format(obj_name))
	printt_dao("\t'''Used for accessing datastore for {} objects.'''".format(obj_name))
	printt_dao("")

def create_init_func(obj_name):
	printt_dao("\tdef __init__(self):")
	printt_dao("\t\tsuper({}DAO, self).__init__('{}DAO')".format(obj_name, obj_name))
	printt_dao("")

def build_insert_sql(obj_name, tbl_schema):
	params = []
	data = []

	for col in tbl_schema["fields"]:
		if col["name"] == "Id":
			continue
		else:
			params.append(col["name"])
			data.append("%({})s".format(uncapitalize(col["name"])))

	params = ", ".join(params)
	data = ", ".join(data)

	printt_dao("\t\tinsertSql = (\"INSERT INTO {} \"".format(obj_name))
	printt_dao("\t\t\t\"({}) \"".format(params))
	printt_dao("\t\t\t\"VALUES ({})\")".format(data))
	printt_dao("")
	printt_dao("\t\tinsertData = {")
	for col in tbl_schema["fields"]:
		if col["name"] == "Id":
			continue
		else:
			printt_dao("\t\t\t'{}' : {}.{},".format(uncapitalize(col["name"]), uncapitalize(obj_name), col["name"]))
	printt_dao("\t\t}")
	printt_dao("")

def create_insert_object_to_db(obj_name, tbl_schema):
	u_obj_name = uncapitalize(obj_name)
	printt_dao("\tdef insert{}(self, {} = None):".format(obj_name, u_obj_name))
	printt_dao("\t\t'''Persists {} to the database.'''".format(u_obj_name))
	printt_dao("\t\tif not {}:".format(u_obj_name))
	printt_dao("\t\t\treturn")
	printt_dao("")
	build_insert_sql(obj_name, tbl_schema)
	printt_dao("\t\treturn self.dbConnection.instance.execute_query(insertSql, insertData)")
	printt_dao("")

def build_update_sql(obj_name, tbl_schema):
	params = []

	for col in tbl_schema["fields"]:
		if col["name"] == "Id":
			continue
		else:
			params.append("{} = %({})s".format(col["name"], uncapitalize(col["name"])))

	params = ", ".join(params)

	printt_dao("\t\tupdateSql = (\"UPDATE {} \"".format(obj_name))
	printt_dao("\t\t\t\"SET {}\"".format(params))
	printt_dao("\t\t\t\"WHERE Id = %(id)s\")")
	printt_dao("")
	printt_dao("\t\tupdateData = {")
	for col in tbl_schema["fields"]:
		printt_dao("\t\t\t'{}' : {}.{},".format(uncapitalize(col["name"]), uncapitalize(obj_name), col["name"]))
	printt_dao("\t\t}")
	printt_dao("")

def create_update_object_to_db(obj_name, tbl_schema):
	u_obj_name = uncapitalize(obj_name)
	printt_dao("\tdef update{}(self, {} = None):".format(obj_name, u_obj_name))
	printt_dao("\t\t'''Updates and persists {} to the database.'''".format(u_obj_name))
	printt_dao("\t\tif not {}:".format(u_obj_name))
	printt_dao("\t\t\treturn")
	printt_dao("")
	build_update_sql(obj_name, tbl_schema)
	printt_dao("\t\treturn self.dbConnection.instance.execute_query(updateSql, updateData)")
	printt_dao("")

def create_delete_object_to_db(obj_name, tbl_schema):
	u_obj_name = uncapitalize(obj_name)

	for col in tbl_schema["fields"]:
		if is_unique(col):
			col_name = col["name"]
			u_col_name = uncapitalize(col_name)

			printt_dao("\tdef deleteBy{}(self, {} = None):".format(col_name, u_col_name))
			printt_dao("\t\t'''Deletes {} object from the database by {}.'''".format(u_obj_name, u_col_name))
			printt_dao("\t\tif not {}:".format(u_col_name))
			printt_dao("\t\t\treturn")
			printt_dao("\t\tdeleteBy{}Sql = \"DELETE FROM {} WHERE {} = {}\".format({})".format(col_name, obj_name, col_name, get_escape_characters(col), u_col_name))
			printt_dao("\t\treturn self.dbConnection.instance.execute_query(deleteBy{}Sql)".format(col_name))
			printt_dao("")

	# Creates delete method by object.
	printt_dao("\tdef deleteBy{}(self, {} = None):".format(obj_name, u_obj_name))
	printt_dao("\t\t'''Deletes {} to the database.'''".format(u_obj_name))
	printt_dao("\t\tif not {}:".format(u_obj_name))
	printt_dao("\t\t\treturn")
	printt_dao("\t\treturn deleteById({}.Id)".format(u_obj_name))
	printt_dao("")

def create_list_objects_of_type(obj_name):
	'''Creates a method that would get all the objects given a limit.'''
	# cursor.fetchmany(int) -> fetches next (int) rows in the table (pagination)
	u_obj_name = uncapitalize(obj_name)
	printt_dao("\tdef getAll{}s(self, limit):".format(obj_name))	
	printt_dao("\t\t'''Returns all {}s.'''".format(u_obj_name))
	printt_dao("\t\tselectSql = \"SELECT * FROM {}\"".format(obj_name))
	printt_dao("")
	printt_dao("\t\tresultSet = self.dbConnection.instance.query_all_result(selectSql)")
	printt_dao("\t\tobjList = []")
	printt_dao("\t\tfor row in resultSet:")
	printt_dao("\t\t\t{} = {}DO.toObj(row)".format(u_obj_name, obj_name))
	printt_dao("\t\t\tobjList.append({})".format(u_obj_name))
	printt_dao("\t\treturn objList")
	printt_dao("")

def create_methods_by_unique_key(obj_name, tbl_schema):
	"""Creates methods for fetching by unique key (e.g. id, name, etc.)."""
	for col in tbl_schema["fields"]:
		if is_unique(col):
			u_obj_name = uncapitalize(obj_name)
			col_name = col["name"]
			u_col_name = uncapitalize(col_name)
			printt_dao("\tdef get{}By{}(self, {}):".format(obj_name, col_name, u_col_name))
			printt_dao("\t\t'''Retrieves {} by {} from the database.'''".format(u_obj_name, u_col_name))
			printt_dao("\t\tselectBy{}Sql = \"SELECT * FROM {} WHERE {} = {}\".format({})".format(col_name, obj_name, col_name, get_escape_characters(col), u_col_name))
			printt_dao("")
			printt_dao("\t\tresultSet = self.dbConnection.instance.query_single_result(selectBy{}Sql)".format(col_name))
			printt_dao("\t\t{} = {}DO.toObj(resultSet)".format(u_obj_name, obj_name))
			printt_dao("\t\treturn {}".format(u_obj_name))
			printt_dao("")


def create_get_objs_for_key(obj_name, tbl_schema):
	"""Creates a getter for list all object being to a key (foreign key.)"""
	u_obj_name = uncapitalize(obj_name)
	for col in tbl_schema["fields"]:
		if "references" in col:
			col_name = col["name"]
			ref_table = col["references"]["ref_table"]
			u_ref_table = uncapitalize(ref_table)
			ref_column = col["references"]["ref_column"]
			printt_dao("\tdef get{}sFor{}(self, {}):".format(obj_name, ref_table, u_ref_table))
			printt_dao("\t\t'''Returns all the {}s belonging to provided {}.'''".format(u_obj_name, u_ref_table))
			printt_dao("\t\tselectSql = \"SELECT * FROM {} WHERE {} = {}\".format({}.{})".format(obj_name, col_name, "{}", u_ref_table, ref_column))
			printt_dao("")
			printt_dao("\t\tresultSet = self.dbConnection.instance.query_all_result(selectSql)")
			printt_dao("\t\tobjList = []")
			printt_dao("\t\tfor row in resultSet:")
			printt_dao("\t\t\t{} = {}DO.toObj(row)".format(u_obj_name, obj_name))
			printt_dao("\t\t\tobjList.append({})".format(u_obj_name))
			printt_dao("\t\treturn objList")
			printt_dao("")

def is_unique(column):
	'''Returns true if column holds unique values'''
	return (("is_unique" in column and column["is_unique"])
				or ("auto_inc" in column and column["auto_inc"])
				or ("is_pk" in column and column["is_pk"]))

def get_escape_characters(column):
	col_type = column["type"]
	if col_type == "bool" or col_type == "int" or col_type == "double":
		return "{}"
	else:
		return "'{}'"

def printt_dao(text = "", colour = cs.DEFAULT):
	# TODO: Fix this.
	if not dao_file:
		printt(text, colour)
	else:
		printt(text, colour, dao_file)

def uncapitalize(name):
	'''Lowercases the first letter of the name.'''
	return name[:1].lower() + name[1:]