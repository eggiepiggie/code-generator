from utils.io_utils import load_json
import json

app_properties = {}

def load_properties():
	global app_properties
	app_properties = load_json("resources/properties.json")

def get_db_properties():
	load_properties()
	db_config = {}
	db_config["dbUsername"] = app_properties["databaseUsername"] if "databaseUsername" in app_properties else None
	db_config["dbPassword"] = app_properties["databasePassword"] if "databasePassword" in app_properties else None
	db_config["dbHost"] = app_properties["databaseHost"] if "databaseHost" in app_properties else None
	db_config["dbName"] = app_properties["databaseName"] if "databaseName" in app_properties else None
	return db_config