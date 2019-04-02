from utils.term_utils import printt, printt_critical, printt_error, printt_warning
from utils.io_utils import load_json
from utils.table_utils import validate_schema
from utils.BaseClassUtils import BaseClassUtils
from datetime import datetime

import resources.cli_styles as cs

'''
	> I think I want this to use flask.request.  It seems a lot neater.
	> We can use toObj() method from the DOs. Translate JSON to DOs.

	@marketApp.route('/foo', methods=['POST']) 
	def foo():
		if not request.json:
			abort(400)
		print request.json
		return json.dumps(request.json)
'''
class RestApiUtils( BaseClassUtils ):

	def __init__(self, objName, toFile = False):
		'''We need to validate that this is a legit object in the json schema.'''
		super(RestApiUtils, self).__init__('RestApiUtils')
		self.objName = objName
		self.uObjName = self.uncapitalize(objName)
		self.dbSchema = self.getSchema(objName)
		self.objSchema = self.dbSchema[objName]
		self.type = "rest_api"
		self.toFile = toFile

	def generateClass(self):
		self.openFile()

		self.generateCommentBlock()
		self.generateImports()
		self.generateGetAll()
		self.generateById()
		self.generateReference()
		self.generateRequestParameterParser()

		self.closeFile()

	def generateCommentBlock(self):
		"""Creates a comment block about the class."""
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#  WARNING: This is an auto-generated file. Do not modify this file.", cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#", cs.PASTEL_YELLOW)
		self.printt_cls("#   {} REST API Class".format(self.objName), cs.PASTEL_YELLOW)
		self.printt_cls("#", cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)
		self.printt_cls("#  Generated on: {ts}".format(ts = str(datetime.now())), cs.PASTEL_YELLOW)
		self.printt_cls("# ===================================================================", cs.PASTEL_YELLOW)

	def generateImports(self):
		"""Creates import statemnts for referencd objects."""
		self.printt_cls("from flask_restful import Resource, reqparse")
		self.printt_cls("from app.bo.{} import {}BO".format(self.objName, self.objName))
		self.printt_cls("from app.dao.{} import {}DAO".format(self.objName, self.uObjName))
		self.printt_cls("")
		self.printt_cls("")

	def generateGetAll(self):
		"""Creates endpoints for get all BO objects."""
		self.printt_cls("class {}GetAll(Resource):".format(self.objName))
		self.printt_cls("")
		self.printt_cls("\tdef get(self):")
		self.printt_cls("\t\t{}s = {}DAO.getAll{}s()".format(self.uObjName, self.uObjName, self.objName))
		self.printt_cls("\t\t{}BOs = [{}BO(do) for do in {}s]".format(self.uObjName, self.objName, self.uObjName))
		self.printt_cls("\t\tboJsonList = [bo.toJson() for bo in {}BOs]".format(self.uObjName))
		self.printt_cls("\t\treturn boJsonList")
		self.printt_cls("")
		self.printt_cls("\tdef post(self):")
		self.printt_cls("\t\targs = getParameters(reqparse.RequestParser())")
		self.printt_cls("\t\t{} = {}BO()".format(self.uObjName, self.objName))
		for col in self.objSchema["fields"]:
			if col["name"] != "Id":
				colName = col["name"]
				self.printt_cls("\t\t{}.set{}(args['{}'])".format(self.uObjName, colName, colName))
		self.printt_cls("\t\t{}.save()".format(self.uObjName))
		self.printt_cls("\t\treturn {}.{}.toJson()".format(self.uObjName, self.uObjName))
		self.printt_cls("")
		self.printt_cls("")

	def generateById(self):
		self.printt_cls("class {}ById(Resource):".format(self.objName))
		self.printt_cls("")
		self.printt_cls("\tdef get(self, {}Id):".format(self.uObjName))
		self.printt_cls("\t\t{}DO = {}DAO.get{}ById({}Id)".format(self.uObjName, self.uObjName, self.objName, self.uObjName))
		self.printt_cls("\t\t{}BO = {}BO({}DO)".format(self.uObjName, self.objName, self.uObjName))
		self.printt_cls("\t\treturn {}BO.toJson()".format(self.uObjName))
		self.printt_cls("")
		self.printt_cls("\tdef put(self, {}Id):".format(self.uObjName))
		self.printt_cls("\t\targs = getParameters(reqparse.RequestParser())")
		self.printt_cls("\t\t{}DO = {}DAO.get{}ById({}Id)".format(self.uObjName, self.uObjName, self.objName, self.uObjName))
		self.printt_cls("\t\t{} = {}BO({}DO)".format(self.uObjName, self.objName, self.uObjName))
		for col in self.objSchema["fields"]:
			if col["name"] != "Id":
				colName = col["name"]
				self.printt_cls("\t\t{}.set{}(args['{}'])".format(self.uObjName, colName, colName))
		self.printt_cls("\t\t{}.update()".format(self.uObjName))
		self.printt_cls("\t\treturn {}.{}.toJson()".format(self.uObjName, self.uObjName))
		self.printt_cls("")
		self.printt_cls("\tdef delete(self, {}Id):".format(self.uObjName))
		self.printt_cls("\t\treturn {}DAO.deleteById({}Id)".format(self.uObjName, self.uObjName))
		self.printt_cls("")
		self.printt_cls("")

	def generateReference(self):
		for obj in self.dbSchema.keys():
			if obj == self.objName:
				continue
			for field in self.dbSchema[obj]["fields"]:
				if "references" in field and field["references"]["ref_table"] == self.objName:
					u_obj = self.uncapitalize(obj)
					self.printt_cls("class {}{}s(Resource):".format(self.objName, obj))
					self.printt_cls("\tdef get(self, {}Id):".format(self.uObjName))
					self.printt_cls("\t\t{}DO = {}DAO.get{}ById({}Id)".format(self.uObjName, self.uObjName, self.objName, self.uObjName))
					self.printt_cls("\t\t{} = {}BO({}DO)".format(self.uObjName, self.objName, self.uObjName))
					self.printt_cls("\t\t{}s = {}.get{}s()".format(u_obj, self.uObjName, obj))
					self.printt_cls("\t\tboJsonList = [c.toJson() for c in {}s]".format(u_obj))
					self.printt_cls("\t\treturn boJsonList")
					self.printt_cls("")
					self.printt_cls("")

	def generateRequestParameterParser(self):
		"""Creates the init function."""
		self.printt_cls("def getParameters(parser):")
		self.printt_cls("\t'''Takes the requests body and returns it as json.'''")
		self.printt_cls("\tparser = reqparse.RequestParser()")
		for col in self.objSchema["fields"]:
			if col["name"] != "Id":
				self.printt_cls("\tparser.add_argument('{}')".format(col["name"]))
		self.printt_cls("\treturn parser.parse_args()")
		self.printt_cls("")

