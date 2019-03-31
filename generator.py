from utils.term_utils import *

import resources.cli_styles as cs
import utils.table_utils as tu
from utils.BoUtils import BoUtils
from utils.DoUtils import DoUtils
from utils.DaoUtils import DaoUtils
from utils.RestApiUtils import RestApiUtils
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
		mode = args[3] if args_count > 3 else None

	if not action:
		printt_error("No action parameter is provided.")

	if action == "--create-table":
		if not obj_name:
			printt_error("No object parameter is provided.")
			prompt()
			return

		if obj_name == "--all":
			tu.create_all()
		else:
			tu.create(obj_name)
	
	elif action == "--drop-table":
		if not obj_name:
			printt_error("No object parameter is provided.")
			prompt()
			return
		tu.drop(obj_name)
	
	elif action == "--create-do-obj":
		if not obj_name:
			printt_error("No object parameter is provided.")
			prompt()
			return
		dou = DoUtils(obj_name, True if mode == "--file" else False)
		dou.generateClass()

	elif action == "--create-dao-obj":
		if not obj_name:
			printt_error("No object parameter is provided.")
			prompt()
			return
		daou = DaoUtils(obj_name, True if mode == "--file" else False)
		daou.generateClass()

	elif action == "--create-bo-obj":
		if not obj_name:
			printt_error("No object parameter is provided.")
			prompt()
			return
		bou = BoUtils(obj_name, True if mode == "--file" else False)
		bou.generateClass()

	elif action == "--create-rest-api":
		if not obj_name:
			printt_error("No object parameter is provided.")
			prompt()
			return
		apiu = RestApiUtils(obj_name, True if mode == "--file" else False)
		apiu.generateClass()

	elif action == "--create-all-obj":
		if not obj_name:
			printt_error("No object parameter is provided.")
			prompt()
			return
		dou = DoUtils(obj_name, True if mode == "--file" else False)
		dou.generateClass()
		daou = DaoUtils(obj_name, True if mode == "--file" else False)
		daou.generateClass()
		bou = BoUtils(obj_name, True if mode == "--file" else False)
		bou.generateClass()
		apiu = RestApiUtils(obj_name, True if mode == "--file" else False)
		apiu.generateClass()

	elif action == "--deploy":
		objList = ['Department', 'Item', 'Purchase', 'PurchaseItemList', 'StockLevel', 'PriceHistory']
		for obj_name in objList:
			dou = DoUtils(obj_name, True)
			dou.generateClass()
			daou = DaoUtils(obj_name, True)
			daou.generateClass()
			bou = BoUtils(obj_name, True)
			bou.generateClass()
			apiu = RestApiUtils(obj_name, True)
			apiu.generateClass()

	elif action == "--help":
		prompt()
	
	else:
		printt_error("Invalid action parameter.")
		prompt()

def prompt():
	printt()
	printt("Eggie's SQL Code Generator", cs.PASTEL_PURPLE)
	printt()
	printt("A simple SQL code generator.", cs.LIGHT_GRAY)
	printt()
	printt("- Print out the help prompt.", cs.PASTEL_GREEN)
	printt("\tgenerator.py --help", cs.PASTEL_BLUE)
	printt()
	printt("- Generate create table SQL statement for object.", cs.PASTEL_GREEN)
	printt("\tgenerator.py --create-table {}<table-name>".format(cs.PASTEL_PINK), cs.PASTEL_BLUE)
	printt()
	printt("- Generate create table SQL statement for all objects.", cs.PASTEL_GREEN)
	printt("\tgenerator.py --create-table {}--all".format(cs.PASTEL_PINK), cs.PASTEL_BLUE)
	printt()
	printt("- Generate drop table SQL statement for object.", cs.PASTEL_GREEN)
	printt("\tgenerator.py --drop-table {}<table-name>".format(cs.PASTEL_PINK), cs.PASTEL_BLUE)
	printt()
	printt("- Generate DO class for object.", cs.PASTEL_GREEN)
	printt("\tgenerator.py --create-do-obj {}<obj-name> <--file>".format(cs.PASTEL_PINK), cs.PASTEL_BLUE)
	printt()
	printt("- Generate DAO class for object.", cs.PASTEL_GREEN)
	printt("\tgenerator.py --create-dao-obj {}<obj-name> <--file>".format(cs.PASTEL_PINK), cs.PASTEL_BLUE)
	printt()
	printt("- Generate BO class for object.", cs.PASTEL_GREEN)
	printt("\tgenerator.py --create-bo-obj {}<obj-name> <--file>".format(cs.PASTEL_PINK), cs.PASTEL_BLUE)
	printt()
	printt("- Generate REST API class for object.", cs.PASTEL_GREEN)
	printt("\tgenerator.py --create-rest-api {}<obj-name> <--file>".format(cs.PASTEL_PINK), cs.PASTEL_BLUE)
	printt()
	printt("- Generate all class for object.", cs.PASTEL_GREEN)
	printt("\tgenerator.py --create-all-obj {}<obj-name> <--file>".format(cs.PASTEL_PINK), cs.PASTEL_BLUE)
	printt()
	printt("- Generate all classes for all object (dangerous!).", cs.PASTEL_GREEN)
	printt("\tgenerator.py --deploy", cs.PASTEL_YELLOW)
	printt()

if __name__ == "__main__":
	main(sys.argv)