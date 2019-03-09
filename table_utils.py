import json_utils as json_u

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

def create(table_name, column_json = None, action = "CMD"):

	# Load database definition.
	dbSchema = load_database_definition();
	tbl_name = "tableName"
	tbl_json = dbSchema[tbl_name]

	generate_comment(tbl_name, tbl_json)
	print("CREATE TABLE " + tbl_name + " (")

	for field in tbl_json["fields"]:
		print("    " + field["name"] + " " + SQL_DATA_TYPES[field["type"]] + ",")

	print(");")
	return True

def drop(table_name, action="CMD"):
	print("DROP TABLE " + table_name + ";")
	return True

def update():
	return True

def generate_comment(table_name, table_json = None):

	print("# ===================================================================")
	print("#  WARNING: This is an auto-generated file. Do not modify this file.")
	print("# ===================================================================")
	print("#")
	print("#  Table Name: " + table_name)
	print("#   -> Columns:")

	for field in table_json["fields"]:
		print("#     -> '" + field["name"] + "' : " + field["type"] + " ")
	
	print("#")
	print("# ===================================================================")
	print("#  Generated on: " + str(datetime.now()))
	print("# ===================================================================")

	return True

def load_database_definition():
	# Reads the database definition and loads it as JSON.
	try:
		with open("resources/database-structure-definition.json") as f:
			db_json = json.load(f)
	except FileNotFoundError as fnf_error:
		print("Error:  Could not load JSON database definition.", fnf_error)

	return db_json