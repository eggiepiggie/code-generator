from flask_restful import Resource, reqparse
from app.dao.Department import departmentDAO
from app.bo.Department import DepartmentBO

class Departments(Resource):

	def get(self):
		result = departmentDAO.getAllDepartments()
		resultList = []
		for r in result:
			resultList.append(r.toJson())
		return resultList

	def post(self):
		args = getParameters(reqparse.RequestParser())
		department = DepartmentBO()
		department.setName(args["Name"])
		department.setDescription(args["Description"])
		department.save()
		return department.department.toJson()


class Department(Resource):

	def get(self, departmentId):
		result = departmentDAO.getDepartmentById(departmentId)
		return result.toJson()

	def put(self, departmentId):
		args = getParameters(reqparse.RequestParser())
		departmentDO = departmentDAO.getDepartmentById(departmentId)
		department = DepartmentBO(departmentDO)
		department.setName(args["Name"])
		department.setDescription(args["Description"])
		department.update()
		return department.department.toJson()

	def delete(self, departmentId):
		return departmentDAO.deleteById(departmentId)


class DepartmentItems(Resource):
	def get(self, departmentId):
		departmentDO = departmentDAO.getDepartmentById(departmentId)
		department = DepartmentBO(departmentDO)
		items = department.getItems()
		result = []
		for r in items:
			result.append(r.toJson())
		return result


def getParameters(parser):
	'''Takes the requests body and returns it as json.'''
	parser = reqparse.RequestParser()
	parser.add_argument("Name")
	parser.add_argument("Description")
	return parser.parse_args()