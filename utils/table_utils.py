from utils.term_utils import printt_critical, printt_error, printt_warning
from datetime import datetime

import json

# TODO #3: Auto-generate insert timestamp

# Defaults for column definitions:
#		- NULL
#		- NO DEFAULT
#		- NO UNIQUE
#		- NO AUTO INCREMENT

SQL_DATA_TYPES = {
	"bool" : 		"BOOLEAN",
	"date" : 		"DATE",
	"double" :		"DOUBLE",
	"int" : 		"INT",
	"str" :			"VARCHAR(255)",
	"text" :		"TEXT",
	"timestamp" :	"TIMESTAMP"
}

def create_all():
	"""Generates CREATE TABLE statements for all tables."""
	return True

def create(tbl_name, column_json = None):
	"""Generates CREATE TABLE statement for specified table."""
	db_schema = load_database_definition()

	if tbl_name not in db_schema:
		printt_error("Object could not be found in table definition json.")
		return

	tbl_json = db_schema[tbl_name]

	create_table_desciption_block(tbl_name, tbl_json)	

	print("CREATE TABLE {table_name} (".format(table_name = tbl_name))
	create_columns(tbl_name, tbl_json)
	#create_unique_constraints(tbl_json)
	#create_pk_constraints(tbl_json)
	create_fk_constraints(tbl_json)
	print(");")

def drop(table_name, action="CMD"):
	print("DROP TABLE {name};".format(name = table_name))

def update():
	return True

def create_table_desciption_block(table_name, table_json = None):
	"""Takes table definition JSON and generate documentation about table."""
	print("# ===================================================================")
	print("#  WARNING: This is an auto-generated file. Do not modify this file.")
	print("# ===================================================================")
	print("#")
	print("#  Table Name: {name}".format(name = table_name))
	print("#   -> Columns:")

	for field in table_json["fields"]:
		print("#     -> '{name}' : {type} ".format(name = field["name"], type = field["type"]))

	print("#")
	print("# ===================================================================")
	print("#  Generated on: {ts}".format(ts = str(datetime.now())))
	print("# ===================================================================")

def load_database_definition():
	"""Loads the database definition and return definition as JSON dictionary."""
	try:
		with open("resources/database-structure-definition.json") as f:
			db_json = json.load(f)
	except FileNotFoundError as fnf_error:
		print("Error: Could not load JSON database definition.", fnf_error)

	return db_json

def create_columns(tbl_name, tbl_json):
	"""Creates column for the given table."""
	for idx, col in enumerate(tbl_json["fields"]):

		comma = "," if idx != 0 else ""
		c_name = ""
		c_type = ""
		c_is_not_null = ""
		c_auto_inc = ""
		c_default = ""
		c_is_unique = ""
		c_is_pk = ""

		if "name" in col:
			c_name = col["name"]

		if "type" in col:
			c_type = SQL_DATA_TYPES[col["type"]]

		if "is_not_null" in col:
			c_is_not_null = col["is_not_null"]
			c_is_not_null = " NOT NULL" if c_is_not_null else ""

		if "auto_inc" in col:
			c_auto_inc = col["auto_inc"]
			c_auto_inc = " AUTO_INCREMENT" if c_auto_inc else ""

		if "default" in col:
			default_value = ""
			if c_type == "INT" or c_type == "BOOLEAN" or c_type == "DOUBLE":
				default_value = str(col["default"]["value"])
			else:
				default_value = "'" + col["default"]["value"] + "'"
			c_default = " DEFAULT " + default_value

		if "is_unique" in col:
			c_is_unique = " UNIQUE"

		if "is_pk" in col:
			c_is_pk = " PRIMARY KEY"

		if not c_name or not c_type:
			printt_error("Name or Type must be provided in column definition for table {}.".format(tbl_name))
			return

		print("\t{comma}{field} {data_type}{is_not_null}{is_unique}{is_pk}{default}{auto_inc}"
			.format(
				comma = comma,
				field = c_name,
				data_type = c_type,
				is_not_null = c_is_not_null,
				is_unique = c_is_unique,
				is_pk = c_is_pk,
				default = c_default,
				auto_inc = c_auto_inc))

def create_unique_constraints(tbl_json):
	"""Generates unique constraints based off database definition for given table."""
	for col in tbl_json["fields"]:
		if "is_unique" in col and col["is_unique"]:
			print("\t,UNIQUE ({})".format(col["name"]))

def create_pk_constraints(tbl_json):
	"""Generates PK constraints based off database definition for given table."""
	for col in tbl_json["fields"]:
		if "is_pk" in col and col["is_pk"]:
			print("\t,PRIMARY KEY ({})".format(col["name"]))

def create_fk_constraints(tbl_json):
	"""Generates FK constraints based off database definition for given table."""
	for col in tbl_json["fields"]:
		if "references" in col:
			column_name = col["name"]
			ref_table = col["references"]["ref_table"]
			ref_column = col["references"]["ref_column"]
			print("\t,FOREIGN KEY ({column_name}) REFERENCES {ref_table}({ref_column})"
				.format(column_name = column_name, ref_table = ref_table, ref_column = ref_column))
