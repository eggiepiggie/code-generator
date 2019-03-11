from utils.term_utils import *

import resources.cli_styles as cs
import utils.table_utils as tu
import sys

def main(args):
	# There can be optional arguments
	args_count = len(args)

	if args_count == 1:
		prompt()
		return
	else:
		action = args[1] if args_count > 1 else None
		obj_name = args[2] if args_count > 2 else None

	if not action:
		printt_error("No action parameter is provided.")

	if action == "--create-table":
		if not obj_name:
			printt_error("No object parameter is provided.")
			prompt()
			return
		tu.create(obj_name)
	
	elif action == "--drop-table":
		if not obj_name:
			printt_error("No object parameter is provided.")
			prompt()
			return
		tu.drop(obj_name)
	
	elif action == "--help":
		prompt()
	
	else:
		printt_error("Invalid action parameter.")
		prompt()

def prompt():
	printt()
	printt("Eggie's SQL Code Generator", cs.PASTEL_PURPLE)
	printt()
	printt("A simple SQL code generator.")
	printt()
	printt("- Print out the help prompt.", cs.PASTEL_GREEN)
	printt("\tgenerator.py --help", cs.PASTEL_BLUE)
	printt()
	printt("- Generate create table SQL statement for object.", cs.PASTEL_GREEN)
	printt("\tgenerator.py --create-table {}<table-name>".format(cs.PASTEL_PINK), cs.PASTEL_BLUE)
	printt()
	printt("- Generate drop table SQL statement for object.", cs.PASTEL_GREEN)
	printt("\tgenerator.py --drop-table {}<table-name>".format(cs.PASTEL_PINK), cs.PASTEL_BLUE)
	printt()

if __name__ == "__main__":
	main(sys.argv)