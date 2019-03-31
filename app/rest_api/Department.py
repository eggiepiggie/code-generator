# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   Department REST API Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.119175
# ===================================================================
from flask_restful import Resource, reqparse
from app.bo.Department import DepartmentBO
from app.dao.Department import departmentDAO


class DepartmentGetAll(Resource):

    def get(self):
        departments = departmentDAO.getAllDepartments()
        departmentsJson = []
        for department in departments:
            departmentsJson.append(department.toJson())
        return departmentsJson

    def post(self):
        args = getParameters(reqparse.RequestParser())
        department = DepartmentBO()
        department.setName(args['Name'])
        department.setDescription(args['Description'])
        department.save()
        return department.department.toJson()


class DepartmentById(Resource):

    def get(self, departmentId):
        department = departmentDAO.getDepartmentById(departmentId)
        return department.toJson()

    def put(self, departmentId):
        args = getParameters(reqparse.RequestParser())
        departmentDO = departmentDAO.getDepartmentById(departmentId)
        department = DepartmentBO(departmentDO)
        department.setName(args['Name'])
        department.setDescription(args['Description'])
        department.update()
        return department.department.toJson()

    def delete(self, departmentId):
        return departmentDAO.deleteById(departmentId)


class DepartmentItems(Resource):
    def get(self, departmentId):
        departmentDO = departmentDAO.getDepartmentById(departmentId)
        department = DepartmentBO(departmentDO)
        items = department.getItems()
        results = []
        for item in items:
            results.append(item.toJson())
        return results


def getParameters(parser):
    '''Takes the requests body and returns it as json.'''
    parser = reqparse.RequestParser()
    parser.add_argument('Name')
    parser.add_argument('Description')
    return parser.parse_args()
