# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   DepartmentDAO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.113608
# ===================================================================
from app.dao.Base import BaseDAO
from app.do.Department import DepartmentDO


class DepartmentDAO( BaseDAO ):
    '''Used for accessing datastore for Department objects.'''

    def __init__(self):
        super(DepartmentDAO, self).__init__('DepartmentDAO')

    def insertDepartment(self, department = None):
        '''Persists department to the database.'''
        if not department:
            return

        insertSql = ("INSERT INTO Department "
            "(Name, Description) "
            "VALUES (%(name)s, %(description)s)")

        insertData = {
            'name' : department.Name,
            'description' : department.Description,
        }

        department.Id = self.dbConnection.instance.insert_one(insertSql, insertData)
        return department

    def updateDepartment(self, department = None):
        '''Updates and persists department to the database.'''
        if not department:
            return

        updateSql = ("UPDATE Department "
            "SET Name = %(name)s, Description = %(description)s"
            "WHERE Id = %(id)s")

        updateData = {
            'id' : department.Id,
            'name' : department.Name,
            'description' : department.Description,
        }

        department.Id = self.dbConnection.instance.update_one(updateSql, updateData)
        return department

    def deleteById(self, id = None):
        '''Deletes department object from the database by id.'''
        if not id:
            return
        deleteByIdSql = "DELETE FROM Department WHERE Id = {}".format(id)
        return self.dbConnection.instance.execute_query(deleteByIdSql)

    def deleteByName(self, name = None):
        '''Deletes department object from the database by name.'''
        if not name:
            return
        deleteByNameSql = "DELETE FROM Department WHERE Name = '{}'".format(name)
        return self.dbConnection.instance.execute_query(deleteByNameSql)

    def deleteByDepartment(self, department = None):
        '''Deletes department to the database.'''
        if not department:
            return
        return self.deleteById(department.Id)

    def getAllDepartments(self, limit = None):
        '''Returns all departments.'''
        selectSql = "SELECT * FROM Department"

        resultSet = self.dbConnection.instance.query_all_result(selectSql)
        objList = []
        for row in resultSet:
            department = DepartmentDO.toObj(row)
            objList.append(department)
        return objList

    def getDepartmentById(self, id):
        '''Retrieves department by id from the database.'''
        selectByIdSql = "SELECT * FROM Department WHERE Id = {}".format(id)

        resultSet = self.dbConnection.instance.query_single_result(selectByIdSql)
        department = DepartmentDO.toObj(resultSet)
        return department

    def getDepartmentByName(self, name):
        '''Retrieves department by name from the database.'''
        selectByNameSql = "SELECT * FROM Department WHERE Name = '{}'".format(name)

        resultSet = self.dbConnection.instance.query_single_result(selectByNameSql)
        department = DepartmentDO.toObj(resultSet)
        return department


departmentDAO = DepartmentDAO()
