from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from utils.table_utils import validate_schema
from datetime import datetime

import resources.cli_styles as cs

def initialize(obj_name):
	"""We need to make sure we have the database schema first."""
	db_schema = load_json("resources/database-structure-definition.json")

	if not validate_schema(db_schema, obj_name):
		return 

	create_object_comment_block(obj_name)
	create_class(obj_name)
	create_init_method(obj_name, db_schema[obj_name])
	create_to_json(obj_name, db_schema[obj_name])
	create_to_obj(obj_name, db_schema[obj_name])
	create_reference_method(obj_name, db_schema[obj_name])
	create_list_referenced_methods(db_schema, obj_name)
	printt("")

def create_object_comment_block(obj_name):
	"""Creates a comment block about the class."""
	printt("# ===================================================================", cs.PASTEL_YELLOW)
	printt("#  WARNING: This is an auto-generated file. Do not modify this file.", cs.PASTEL_YELLOW)
	printt("# ===================================================================", cs.PASTEL_YELLOW)
	printt("#", cs.PASTEL_YELLOW)
	printt("#   {}DO Class".format(obj_name), cs.PASTEL_YELLOW)
	printt("#", cs.PASTEL_YELLOW)
	printt("# ===================================================================", cs.PASTEL_YELLOW)
	printt("#  Generated on: {ts}".format(ts = str(datetime.now())), cs.PASTEL_YELLOW)
	printt("# ===================================================================", cs.PASTEL_YELLOW)

def create_class(obj_name):
	printt("import json")
	printt("import utils.db_utils as db")
	printt("")
	printt("")
	printt("class {}DO:".format(obj_name))

def create_init_method(obj_name, tbl_schema):
	"""Creates constructor method for given object."""

	# Generates list of parameters that corresponds to the fields of the object
	init_params = "self"
	for col in tbl_schema["fields"]:
		init_params += ", {}".format(uncapitalize(col["name"]))

	printt("\tdef __init__({}):".format(init_params))
	for col in tbl_schema["fields"]:
		name = col["name"]
		printt("\t\tself.{} = {}".format(name, uncapitalize(name)))
	printt("")

def create_to_json(obj_name, tbl_schema):
	'''Generates a method for converting object to json for serialization.'''
	printt("\tdef toJson(self, simple = False):")
	printt("\t\tobjJson = {}")
	printt("\t\tif simple:")
	printt("\t\t\tobjJson['Id'] = self.Id")
	printt("\t\telse:")
	for col in tbl_schema["fields"]:
		printt("\t\t\tobjJson['{}'] = self.{}".format(col["name"], col["name"]))
	printt("\t\treturn json.dumps(objJson)")
	printt("")

def create_to_obj(obj_name, tbl_schema):
	'''Generates a method for converting a json into specified object.'''
	printt("\tdef toObj(self, objJson = {}):")
	printt("\t\t{} = {}()".format(obj_name.lower(), obj_name))
	for col in tbl_schema["fields"]:
		printt("\t\t{}.{} = objJson['{}'] if '{}' in objJson else None".format(obj_name.lower(), col["name"], col["name"], col["name"]))
	printt("\t\treturn {}".format(obj_name.lower()))
	printt("")

def create_reference_method(obj_name, tbl_schema):
	"""Creates update methods for fields that are mapped to another object."""
	for col in tbl_schema["fields"]:
		if "references" in col:
			column_name = col["name"]
			ref_table = col["references"]["ref_table"]
			ref_column = col["references"]["ref_column"]
			printt("\tdef update{}(self, {}):".format(ref_table, uncapitalize(ref_table)))
			printt("\t\tself.{} = {}.{}".format(column_name, uncapitalize(ref_table), ref_column))
			printt("")

def create_list_referenced_methods(db_schema, obj_name):
	"""Creates a method that list all objects that FK to this object."""
	for obj in db_schema.keys():
		if obj == obj_name:
			continue
		for field in db_schema[obj]["fields"]:
			if "references" in field and field["references"]["ref_table"] == obj_name:
				u_obj_name = uncapitalize(obj)
				printt("\tdef get{}s(self):".format(obj))
				printt("\t\t#TODO: Returns {}s belonging to this {}.".format(u_obj_name, uncapitalize(obj_name)))
				printt("\t\treturn True")
				printt("")

def uncapitalize(name):
	"""Lowercases the first letter of the name."""
	return name[:1].lower() + name[1:]