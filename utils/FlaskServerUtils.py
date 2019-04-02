from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from utils.table_utils import validate_schema
from utils.BaseClassUtils import BaseClassUtils
from datetime import datetime

import resources.cli_styles as cs

class FlaskServerUtils( BaseClassUtils ):

	def __init__(self, objName, appName = None, toFile = False):
		'''We need to validate that this is a legit object in the json schema.'''
		super(FlaskServerUtils, self).__init__('FlaskServerUtils')
		self.appName = appName
		self.v_appName = self.uncapitalize(appName)
		self.objName = objName
		self.uObjName = self.uncapitalize(objName)
		self.dbSchema = self.getSchema(objName)
		self.objSchema = self.dbSchema[objName]
		self.type = "flask_server"
		self.toFile = toFile

	def generateClass(self):
		#self.boFile = open('app/{}/{}Server.py'.format(self.type, self.appName), 'w')
		self.boFile = open('{}Server.py'.format(self.appName), 'w')

		self.generateCommentBlock()
		self.generateImports()
		self.generateServer()
		self.generateApiResources()
		self.generateMain()

		self.boFile.close()

	def generateCommentBlock(self):
		"""Creates a comment block about the class."""
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#  WARNING: This is an auto-generated file. Do not modify this file.", cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#", cs.PASTEL_YELLOW)
		self.printt_cls("#   Market Flask Server", cs.PASTEL_YELLOW)
		self.printt_cls("#", cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#  Generated on: {ts}".format(ts = str(datetime.now())), cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)

	def generateImports(self):
		"""Creates import statements."""
		self.printt_cls("from flask import Flask, request")
		self.printt_cls("from flask_restful import Api")
		self.printt_cls("")
		for obj in self.dbSchema.keys():
			self.printt_cls("from app.rest_api.{} import *".format(obj))
		self.printt_cls("")

	def generateServer(self):
		'''Creates code for generating Flask server API.'''
		self.printt_cls("{}App = Flask(__name__)".format(self.v_appName))
		self.printt_cls("{}Api = Api({}App)".format(self.v_appName, self.v_appName))
		self.printt_cls("")

	def generateApiResources(self):
		'''Creates Resource for all the different objects.'''
		for obj in self.dbSchema.keys():
			u_obj = self.uncapitalize(obj)
			self.printt_cls("# ---------------------------------------------------------")
			self.printt_cls("#   {} REST API".format(obj))
			self.printt_cls("# ---------------------------------------------------------")
			self.printt_cls("{}Api.add_resource( {}GetAll, '/{}' )".format(self.v_appName, obj, u_obj))
			self.printt_cls("{}Api.add_resource( {}ById, '/{}/<int:{}Id>' )".format(self.v_appName, obj, u_obj, u_obj))
			for inner_obj in self.dbSchema.keys():
				if inner_obj == obj:
					continue
				for field in self.dbSchema[inner_obj]["fields"]:
					if "references" in field and field["references"]["ref_table"] == obj:
						u_inner_obj = self.uncapitalize(inner_obj)
						self.printt_cls("{}Api.add_resource( {}{}s, '/{}/<int:{}Id>/{}' )".format(self.v_appName, obj, inner_obj, u_obj, u_obj, u_inner_obj))
			self.printt_cls("")
		self.printt_cls("")

	def generateMain(self):
		'''Creates main method.'''
		# TODO: we probably want to pass in the port number for the Flask server.
		self.printt_cls("if __name__ == '__main__':")
		self.printt_cls("\t{}App.run(port = '5000')".format(self.v_appName))
		self.printt_cls("")

