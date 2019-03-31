from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from utils.table_utils import validate_schema
from datetime import datetime

import resources.cli_styles as cs

do_file = None

def initialize(obj_name, to_file = False):
	"""We need to make sure we have the database schema first."""
	db_schema = load_json("resources/database-structure-definition.json")

	if not validate_schema(db_schema, obj_name):
		return 

	if to_file:
		global do_file
		do_file = open('app/do/{}.py'.format(obj_name), 'w')

	create_object_comment_block(obj_name)
	create_class(obj_name)
	create_init_method(obj_name, db_schema[obj_name])
	create_to_json(obj_name, db_schema[obj_name])
	create_to_string(obj_name, db_schema[obj_name])
	create_equals_to(obj_name, db_schema[obj_name])
	create_to_obj(obj_name, db_schema[obj_name])
	printt_do("")

	if to_file:
		do_file.close()

def create_object_comment_block(obj_name):
	"""Creates a comment block about the class."""
	printt_do("# ===================================================================", cs.PASTEL_YELLOW)
	printt_do("#  WARNING: This is an auto-generated file. Do not modify this file.", cs.PASTEL_YELLOW)
	printt_do("# ===================================================================", cs.PASTEL_YELLOW)
	printt_do("#", cs.PASTEL_YELLOW)
	printt_do("#   {}DO Class".format(obj_name), cs.PASTEL_YELLOW)
	printt_do("#", cs.PASTEL_YELLOW)
	printt_do("# ===================================================================", cs.PASTEL_YELLOW)
	printt_do("#  Generated on: {ts}".format(ts = str(datetime.now())), cs.PASTEL_YELLOW)
	printt_do("# ===================================================================", cs.PASTEL_YELLOW)

def create_class(obj_name):
	printt_do("from app.do.Base import BaseDO")
	printt_do("")
	printt_do("")
	printt_do("class {}DO( BaseDO ):".format(obj_name))

def create_init_method(obj_name, tbl_schema):
	"""Creates constructor method for given object."""

	# Generates list of parameters that corresponds to the fields of the object
	init_params = "self"
	for col in tbl_schema["fields"]:
		init_params += ", {} = None".format(uncapitalize(col["name"]))

	printt_do("\tdef __init__({}):".format(init_params))
	for col in tbl_schema["fields"]:
		name = col["name"]
		printt_do("\t\tself.{} = {}".format(name, uncapitalize(name)))
	printt_do("")

def create_to_json(obj_name, tbl_schema):
	'''Generates a method for converting object to json for serialization.'''
	printt_do("\tdef toJson(self, simple = False):")
	printt_do("\t\t'''Converts this object into a json.'''")
	printt_do("\t\tobjJson = {}")
	printt_do("\t\tif simple:")
	printt_do("\t\t\tobjJson['Id'] = self.Id")
	printt_do("\t\telse:")
	for col in tbl_schema["fields"]:
		printt_do("\t\t\tobjJson['{}'] = self.{}".format(col["name"], col["name"]))
	printt_do("\t\treturn objJson")
	printt_do("")

def create_to_string(obj_name, tbl_schema):
	'''Generates a method for creating string representation of objects.'''
	printt_do("\tdef toString(self):")
	printt_do("\t\t'''Generates a string representation of this object.'''")
	params = []
	data = []
	for col in tbl_schema["fields"]:
		u_col_name = uncapitalize(col["name"])
		params.append("{}={}".format(u_col_name, "{}"))
		data.append("self.{}".format(col["name"]))
	params = ", ".join(params)
	data = ", ".join(data)
	printt_do("\t\treturn \"{}DO[{}]\".format({})".format(obj_name, params, data))
	printt_do("")


def create_equals_to(obj_name, tbl_schema):
	'''Generates a method for comparing one object to another object.'''
	u_obj_name = uncapitalize(obj_name)
	printt_do("\tdef equalsTo(self, {}):".format(u_obj_name))
	printt_do("\t\t'''Compares this object with another object to see if they are equal.'''")
	for col in tbl_schema["fields"]:
		col_name = col["name"]
		if col_name == "Id":
			continue
		printt_do("\t\tif self.{} != {}.{}:".format(col_name, u_obj_name, col_name))
		printt_do("\t\t\treturn False")
	printt_do("\t\treturn True")
	printt_do("")

def create_to_obj(obj_name, tbl_schema):
	'''Generates a method for converting a json into specified object.'''
	printt_do("\t@classmethod")
	printt_do("\tdef toObj(self, objJson = {}):")
	printt_do("\t\t'''Converts json into a object.'''")
	printt_do("\t\t{} = {}()".format(obj_name.lower(), obj_name))
	for col in tbl_schema["fields"]:
		printt_do("\t\t{}.{} = objJson['{}'] if '{}' in objJson else None".format(obj_name.lower(), col["name"], col["name"], col["name"]))
	printt_do("\t\treturn {}".format(obj_name.lower()))
	printt_do("")

def printt_do(text = "", colour = cs.DEFAULT):
	# TODO: Fix this.
	if not do_file:
		printt(text, colour)
	else:
		printt(text, colour, do_file)

def uncapitalize(name):
	"""Lowercases the first letter of the name."""
	return name[:1].lower() + name[1:]