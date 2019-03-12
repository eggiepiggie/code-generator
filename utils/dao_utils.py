
def create_list_objects_of_type(obj_name):	
	print("\tdef list{}s(self, limit):".format(obj_name))	
	print("\t\t#TODO: Returns all {}s.".format(uncapitalize(obj_name)))
	print("\t\treturn True")
	print("")

def create_methods_by_unique_key(obj_name, tbl_schema):
	"""Creates methods for fetching by unique key (e.g. id, name, etc.)."""
	for col in tbl_schema["fields"]:
		if ("is_unique" in col and col["is_unique"]) or ("auto_inc" in col and col["auto_inc"]):
			column_name = col["name"]
			print("\tdef get{}By{}(self, {}):".format(obj_name, column_name, uncapitalize(column_name)))
			print("\t\t# TODO: Gets {} by {}.".format(obj_name, column_name))
			print("\t\treturn True")
			print("")

def uncapitalize(name):
	"""Lowercases the first letter of the name."""
	return name[:1].lower() + name[1:]