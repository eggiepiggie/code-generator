from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from datetime import datetime

import resources.cli_styles as cs

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
	db_schema = load_database_definition()
	print("")
	for tbl_name in db_schema.keys():
		create(tbl_name)
		print("")


def create(tbl_name):
	"""Generates CREATE TABLE statement for specified table."""
	db_schema = load_database_definition()

	if not validate_schema(db_schema, tbl_name):
		return

	tbl_json = db_schema[tbl_name]
	create_table_desciption_block(tbl_name, tbl_json)	
	printt("CREATE TABLE {tbl_name} (".format(tbl_name = tbl_name), cs.PASTEL_PURPLE)
	create_columns(tbl_name, tbl_json)
	create_fk_constraints(db_schema, tbl_json)
	printt(");", cs.PASTEL_PURPLE)

def drop(tbl_name):
	print("DROP TABLE {name};".format(name = tbl_name))

def load_database_definition():
	"""Loads the database definition and return definition as JSON dictionary."""
	return load_json("resources/database-structure-definition.json")

def create_table_desciption_block(tbl_name, table_json = None):
	"""Takes table definition JSON and generate documentation about table."""
	printt("# ===================================================================", cs.PASTEL_YELLOW)
	printt("#  WARNING: This is an auto-generated file. Do not modify this file.", cs.PASTEL_YELLOW)
	printt("# ===================================================================", cs.PASTEL_YELLOW)
	printt("#", cs.PASTEL_YELLOW)
	printt("#  Table Name: {name}".format(name = tbl_name), cs.PASTEL_YELLOW)

	for field in table_json["fields"]:
		printt("#\t-> '{name}' : {type} ".format(name = field["name"], type = field["type"]), cs.PASTEL_YELLOW)

	printt("#", cs.PASTEL_YELLOW)
	printt("# ===================================================================", cs.PASTEL_YELLOW)
	printt("#  Generated on: {ts}".format(ts = str(datetime.now())), cs.PASTEL_YELLOW)
	printt("# ===================================================================", cs.PASTEL_YELLOW)

def create_columns(tbl_name, tbl_json):
	"""Creates column for the given table."""
	for idx, col in enumerate(tbl_json["fields"]):

		comma = "," if idx != 0 else ""
		c_name = col["name"]
		c_type = SQL_DATA_TYPES[col["type"]]
		c_is_not_null = ""
		c_auto_inc = ""
		c_default = ""
		c_is_unique = ""
		c_is_pk = ""

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

		print("\t{comma}{field} {data_type}{is_not_null}{is_unique}{is_pk}{default}{auto_inc}"
			.format(
				comma = comma,
				field = cs.PASTEL_PINK + c_name,
				data_type = cs.PASTEL_BLUE + c_type,
				is_not_null = c_is_not_null,
				is_unique = c_is_unique,
				is_pk = c_is_pk,
				default = c_default,
				auto_inc = c_auto_inc + cs.DEFAULT))

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

def create_fk_constraints(db_schema, tbl_json):
	"""Generates FK constraints based off database definition for given table."""
	for col in tbl_json["fields"]:
		if "references" in col:
			column_name = col["name"]
			ref_table = col["references"]["ref_table"]
			ref_column = col["references"]["ref_column"]
			print("\t,FOREIGN KEY ({column_name}) REFERENCES {ref_table}({ref_column})"
				.format(column_name = column_name, ref_table = ref_table, ref_column = ref_column))

# ==========================================
#   Validator methods
# ==========================================
def validate_schema(db_schema, tbl_name):
	"""Validates that the table schema is sensible."""

	# Validates that table exists.
	if tbl_name not in db_schema:
		printt_error("'{}' object could not be found in table definition json.".format(tbl_name))
		return False

	# Validates that columns are sensible.
	tbl_json = db_schema[tbl_name]
	for col in tbl_json["fields"]:

		# Validates that the name exists.
		if not col["name"]:
			printt_error("Name must be provided in column definition for table '{}'.".format(tbl_name))
			return False
		
		# Validates that the data type exists.
		if not col["type"] or col["type"] not in SQL_DATA_TYPES:
			printt_error("Valid type must be provided for '{}' column in table '{}'.".format(col["name"], tbl_name))
			return False

		# Validates there is a default value for column.
		if "default" in col and "value" not in col["default"]:
			printt_error("A default value must be provided for column '{}' in '{}'.".format(col["name"], tbl_name))
			return False

		# Validates that FK is a valid entity in the db schema.
		if "references" in col:
			column_name = col["name"]
			ref_table = col["references"]["ref_table"]
			ref_column = col["references"]["ref_column"]
			if ref_table in db_schema:
				if not any(x for x in db_schema[ref_table]["fields"] if x["name"] == ref_column):
					printt_error("'{}' table does have '{}' column.".format(ref_table, ref_column))
					return False
			else:
				printt_error("'{}' table does not exists.".format(ref_table))
				return False
	return True