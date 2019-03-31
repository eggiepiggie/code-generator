from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from utils.table_utils import validate_schema
from datetime import datetime

import resources.cli_styles as cs

bo_file = None

def initialize(obj_name, to_file = False):
	"""We need to make sure we have the database schema first."""
	db_schema = load_json("resources/database-structure-definition.json")

	if not validate_schema(db_schema, obj_name):
		return

	if to_file:
		global bo_file
		bo_file = open('app/bo/{}.py'.format(obj_name), 'w')

	create_object_comment_block(obj_name)
	get_external_imports(db_schema, obj_name)
	create_class(obj_name)
	create_init(obj_name)
	create_getters_setters(obj_name, db_schema[obj_name])
	create_crud_functions(obj_name)
	create_list_referenced_methods(db_schema, obj_name)

	if to_file:
		bo_file.close()

def create_object_comment_block(obj_name):
	"""Creates a comment block about the class."""
	printt_bo("# ===================================================================", cs.PASTEL_YELLOW)
	printt_bo("#  WARNING: This is an auto-generated file. Do not modify this file.", cs.PASTEL_YELLOW)
	printt_bo("# ===================================================================", cs.PASTEL_YELLOW)
	printt_bo("#", cs.PASTEL_YELLOW)
	printt_bo("#   {}BO Class".format(obj_name), cs.PASTEL_YELLOW)
	printt_bo("#", cs.PASTEL_YELLOW)
	printt_bo("# ===================================================================", cs.PASTEL_YELLOW)
	printt_bo("#  Generated on: {ts}".format(ts = str(datetime.now())), cs.PASTEL_YELLOW)
	printt_bo("# ===================================================================", cs.PASTEL_YELLOW)

def create_class(obj_name):
	"""Creates class signature."""
	printt_bo("class {}BO( BaseBO ):".format(obj_name))
	printt_bo("\t'''Used for representing a business object {}.'''".format(uncapitalize(obj_name)))
	printt_bo("")

def get_external_imports(db_schema, obj_name):
	"""Creates import statemnts for referencd objects."""
	u_obj_name = uncapitalize(obj_name)
	printt_bo("from app.bo.Base import BaseBO")
	printt_bo("from app.do.{} import {}DO".format(obj_name, obj_name))
	printt_bo("")
	printt_bo("from app.dao.{} import {}DAO".format(obj_name, u_obj_name))
	for obj in db_schema.keys():
		if obj == obj_name:
			continue
		for field in db_schema[obj]["fields"]:
			if "references" in field and field["references"]["ref_table"] == obj_name:
				printt_bo("from app.dao.{} import {}DAO".format(obj, uncapitalize(obj)))
	printt_bo("")
	printt_bo("")

def create_init(obj_name):
	"""Creates the init function. Must accept a valid DO object."""
	u_obj_name = uncapitalize(obj_name)
	printt_bo("\tdef __init__(self, {}):".format(uncapitalize(obj_name)))
	printt_bo("\t\t'''Must accept a valid {}DO object.'''".format(obj_name))
	printt_bo("\t\tsuper({}BO, self).__init__('{}BO')".format(obj_name, obj_name))
	printt_bo("\t\tself.{} = {}".format(u_obj_name, u_obj_name))
	printt_bo("")

def create_getters_setters(obj_name, tbl_schema):
	"""Creates getters and setters for every field of the object."""
	u_obj_name = uncapitalize(obj_name)
	printt_bo("\t# ==================================")
	printt_bo("\t#  Property Functions")
	printt_bo("\t# ==================================")
	for col in tbl_schema["fields"]:
		col_name = col["name"]
		u_col_name = uncapitalize(col_name)
		if col_name == "Id":
			continue
		printt_bo("\tdef get{}(self):".format(col_name))
		printt_bo("\t\treturn self.{}.{}".format(u_obj_name, col_name))
		printt_bo("")
		printt_bo("\tdef set{}(self, {}):".format(col_name, u_col_name))
		printt_bo("\t\tself.{}.{} = {}".format(u_obj_name, col_name, u_col_name))
		printt_bo("")

def create_crud_functions(obj_name):
	"""Creates CRUD functions for the object."""
	u_obj_name = uncapitalize(obj_name)

	printt_bo("\t# ==================================")
	printt_bo("\t#  CRUD Functions")
	printt_bo("\t# ==================================")
	printt_bo("\tdef save(self):")
	printt_bo("\t\treturn {}DAO.insert{}(self.{})".format(u_obj_name, obj_name, u_obj_name))
	printt_bo("")
	printt_bo("\tdef update(self):")
	printt_bo("\t\treturn {}DAO.update{}(self.{})".format(u_obj_name, obj_name, u_obj_name))
	printt_bo("")
	printt_bo("\tdef delete(self):")
	printt_bo("\t\treturn {}DAO.deleteBy{}(self.{})".format(u_obj_name, obj_name, u_obj_name))
	printt_bo("")

def create_list_referenced_methods(db_schema, obj_name):
	"""Creates a method that list all objects that FK to this object."""
	u_obj_name = uncapitalize(obj_name)
	for obj in db_schema.keys():
		if obj == obj_name:
			continue
		for field in db_schema[obj]["fields"]:
			if "references" in field and field["references"]["ref_table"] == obj_name:
				u_obj = uncapitalize(obj)
				printt_bo("\tdef get{}s(self):".format(obj))
				printt_bo("\t\t'''Returns {}s belonging to this {}.'''".format(u_obj, u_obj_name))
				printt_bo("\t\tself.{}s = {}DAO.get{}sFor{}(self.{})".format(u_obj, u_obj, obj, obj_name, u_obj_name))
				printt_bo("\t\treturn self.{}s".format(u_obj))
				printt_bo("")
				printt_bo("\tdef add{}(self, {}):".format(obj, u_obj))
				printt_bo("\t\tself.{}s.append({})".format(u_obj, u_obj))
				printt_bo("")
				printt_bo("\tdef remove{}(self, {}):".format(obj, u_obj))
				printt_bo("\t\tself.{}s.remove({})".format(u_obj, u_obj))
				printt_bo("")

def printt_bo(text = "", colour = cs.DEFAULT):
	# TODO: Fix this.
	if not bo_file:
		printt(text, colour)
	else:
		printt(text, colour, bo_file)

def uncapitalize(name):
	'''Lowercases the first letter of the name.'''
	return name[:1].lower() + name[1:]