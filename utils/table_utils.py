from utils.term_utils import printt_critical, printt_error, printt_warning
from datetime import datetime

import json

# TODO #1: We could have each of these functions to take in a parameter. CMD or FILE
# TODO #2: Auto-generate Id column
# TODO #3: Auto-generate insert timestamp
# TODO #4: Auto-generate NOT NULL
# TODO #5: Auto-generate UNIQUE
SQL_DATA_TYPES = {
	"str" :			"VARCHAR(255)",
	"int" : 		"INT",
	"date" : 		"DATE",
	"timestamp" :	"TIMESTAMP"
}

def create_all():
	"""Generates CREATE TABLE statements for all tables."""
	return True

def create(table_name, column_json = None, action = "CMD"):
	"""Generates CREATE TABLE statement for specified table."""
	# Load database definition.
	db_schema = load_database_definition()

	if table_name not in db_schema:
		printt_error("Object could not be found in table definition json.")
		return

	tbl_json = db_schema[table_name]

	generate_comment(table_name, tbl_json)	
	print("CREATE TABLE {table_name} (".format(table_name = table_name))

	for field in tbl_json["fields"]:

		col_name = field["name"]
		col_type = SQL_DATA_TYPES[field["type"]]
		col_is_null = "NULL" if field["is_null"] else "NOT NULL"
		col_auto_inc = "AUTO_INCREMENT"if field["auto_inc"] else ""

		print("\t{field} {data_type} {is_null} {auto_inc},"
			.format(field = col_name, data_type = col_type, is_null = col_is_null, auto_inc = col_auto_inc))

	print(");")

def drop(table_name, action="CMD"):
	print("DROP TABLE {name};".format(name = table_name))

def update():
	return True

def generate_comment(table_name, table_json = None):
	"""Takes table definition JSON and generate documentation about table."""
	print("# ===================================================================")
	print("#  WARNING: This is an auto-generated file. Do not modify this file.")
	print("# ===================================================================")
	print("#")
	print("#  Table Name: {name}".format(name = table_name))
	print("#   -> Columns:")

	for field in table_json["fields"]:
		field_name = field["name"]
		field_type = field["type"]
		print("#     -> '{name}' : {type} ".format(name = field_name, type = field_type))
	
	print("#")
	print("# ===================================================================")
	print("#  Generated on: {ts}".format(ts = str(datetime.now())))
	print("# ===================================================================")

	return True

def load_database_definition():
	"""Loads the database definition and return definition as JSON dictionary."""
	try:
		with open("resources/database-structure-definition.json") as f:
			db_json = json.load(f)
	except FileNotFoundError as fnf_error:
		print("Error: Could not load JSON database definition.", fnf_error)

	return db_json