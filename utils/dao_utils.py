from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from utils.table_utils import validate_schema
import utils.db_utils as dbu
from datetime import datetime

import resources.cli_styles as cs

def initialize(obj_name):
	"""We need to make sure we have the database schema first."""
	db_schema = load_json("resources/database-structure-definition.json")

	if not validate_schema(db_schema, obj_name):
		return 

	create_object_comment_block(obj_name)
	create_class(obj_name)
	create_insert_object_to_db(obj_name, db_schema[obj_name])
	create_update_object_to_db(obj_name, db_schema[obj_name])
	create_delete_object_to_db(obj_name, db_schema[obj_name])
	create_list_objects_of_type(obj_name)
	create_methods_by_unique_key(obj_name, db_schema[obj_name])
	printt("")

def create_object_comment_block(obj_name):
	"""Creates a comment block about the class."""
	printt("# ===================================================================", cs.PASTEL_YELLOW)
	printt("#  WARNING: This is an auto-generated file. Do not modify this file.", cs.PASTEL_YELLOW)
	printt("# ===================================================================", cs.PASTEL_YELLOW)
	printt("#", cs.PASTEL_YELLOW)
	printt("#   {}DAO Class".format(obj_name), cs.PASTEL_YELLOW)
	printt("#", cs.PASTEL_YELLOW)
	printt("# ===================================================================", cs.PASTEL_YELLOW)
	printt("#  Generated on: {ts}".format(ts = str(datetime.now())), cs.PASTEL_YELLOW)
	printt("# ===================================================================", cs.PASTEL_YELLOW)

def create_class(obj_name):
	printt("import json")
	printt("import utils.db_utils as db")
	printt("")
	printt("")
	printt("class {}DAO:".format(obj_name))

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

	printt("\t\tinsert_sql = (\"INSERT INTO {} \"".format(obj_name))
	printt("\t\t\t\"({}) \"".format(params))
	printt("\t\t\t\"VALUES ({})\")".format(data))
	printt("")
	printt("\t\tinsert_data = {")
	for col in tbl_schema["fields"]:
		if col["name"] == "Id":
			continue
		else:
			printt("\t\t\t'{}' : {}.{},".format(uncapitalize(col["name"]), uncapitalize(obj_name), col["name"]))
	printt("\t\t}")
	printt("")

def create_insert_object_to_db(obj_name, tbl_schema):
	printt("\tdef insert{}({} = None):".format(obj_name, uncapitalize(obj_name)))
	printt("\t\tif not {}:".format(uncapitalize(obj_name)))
	printt("\t\t\treturn")
	printt("")
	build_insert_sql(obj_name, tbl_schema)
	printt("\t\tcursor = dbu.db_connection.cursor()")
	printt("\t\tcursor.execute(insert_sql, insert_data)")
	printt("\t\tdbu.db_connection.commit()")
	printt("\t\tcursor.close()")
	printt("")

def build_update_sql(obj_name, tbl_schema):
	params = []

	for col in tbl_schema["fields"]:
		if col["name"] == "Id":
			continue
		else:
			params.append("{} = %({})s".format(col["name"], uncapitalize(col["name"])))

	params = ", ".join(params)

	printt("\t\tupdate_sql = (\"UPDATE {} \"".format(obj_name))
	printt("\t\t\t\"SET {}".format(params))
	printt("\t\t\t\"WHERE Id = %(id)s\")")
	printt("")
	printt("\t\tupdate_data = {")
	for col in tbl_schema["fields"]:
		printt("\t\t\t'{}' : {}.{},".format(uncapitalize(col["name"]), uncapitalize(obj_name), col["name"]))
	printt("\t\t}")
	printt("")

def create_update_object_to_db(obj_name, tbl_schema):
	printt("\tdef update{}({} = None):".format(obj_name, uncapitalize(obj_name)))
	printt("\t\tif not {}:".format(uncapitalize(obj_name)))
	printt("\t\t\treturn")
	printt("")
	build_update_sql(obj_name, tbl_schema)
	printt("\t\tcursor = dbu.db_connection.cursor()")
	printt("\t\tcursor.execute(update_sql, update_data)")
	printt("\t\tdbu.db_connection.commit()")
	printt("\t\tcursor.close()")
	printt("")

def create_delete_object_to_db(obj_name, tbl_schema):
	u_obj_name = uncapitalize(obj_name)

	for col in tbl_schema["fields"]:
		if is_unique(col):
			col_name = col["name"]
			u_col_name = uncapitalize(col_name)

			printt("\t@staticmethod")
			printt("\tdef deleteBy{}({} = None):".format(col_name, u_col_name))
			printt("\t\tif not {}:".format(u_col_name))
			printt("\t\t\treturn")
			printt("")
			printt("\t\tdeleteBy{}Sql = \"DELETE FROM {} WHERE {} = %s\"".format(col_name, obj_name, col_name))
			printt("")
			printt("\t\tcursor = dbu.db_connection.cursor()")
			printt("\t\tcursor.execute(deleteBy{}Sql, ({}))".format(col_name, u_col_name))
			printt("\t\tdbu.db_connection.commit()")
			printt("\t\tcursor.close()")
			printt("")

	# Creates delete method by object.
	printt("\t@staticmethod")
	printt("\tdef deleteBy{}({} = None):".format(obj_name, u_obj_name))
	printt("\t\tif not {}:".format(u_obj_name))
	printt("\t\t\treturn")
	printt("\t\tdeleteById({}.Id)".format(u_obj_name))
	printt("")

def create_list_objects_of_type(obj_name):
	'''Creates a method that would get all the objects given a limit.'''
	printt("\tdef list{}s(self, limit):".format(obj_name))	
	printt("\t\t#TODO: Returns all {}s.".format(uncapitalize(obj_name)))
	printt("\t\treturn True")
	printt("")

def create_methods_by_unique_key(obj_name, tbl_schema):
	"""Creates methods for fetching by unique key (e.g. id, name, etc.)."""
	for col in tbl_schema["fields"]:
		if ("is_unique" in col and col["is_unique"]) or ("auto_inc" in col and col["auto_inc"]):
			column_name = col["name"]
			printt("\t@staticmethod")
			printt("\tdef get{}By{}(self, {}):".format(obj_name, column_name, uncapitalize(column_name)))
			printt("\t\t# TODO: Gets {} by {}.".format(obj_name, column_name))
			printt("\t\treturn True")
			printt("")

def is_unique(column):
	'''Returns true if column holds unique values'''
	return (("is_unique" in column and column["is_unique"])
				or ("auto_inc" in column and column["auto_inc"])
				or ("is_pk" in column and column["is_pk"]))

def uncapitalize(name):
	'''Lowercases the first letter of the name.'''
	return name[:1].lower() + name[1:]