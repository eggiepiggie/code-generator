from app.dao.Base import BaseDAO

class DepartmentDAO( BaseDAO ):

    def __init__(self):
        super(DepartmentDAO, self).__init__("DepartmentDAO")
        if not self.dbConnection.instance.query_table_exists("Department"):
            sqlQuery = ("CREATE TABLE Department ("
                        "Id INT PRIMARY KEY AUTO_INCREMENT"
                        ",Name VARCHAR(255) NOT NULL UNIQUE"
                        ",Description TEXT"
                        ");")
            self.dbConnection.instance.execute_query(sqlQuery)

    def insertDepartment(self, department = None):
        if not department:
            return

        insertSql = ("INSERT INTO Department "
            "(Name, Description) "
            "VALUES (%(name)s, %(description)s)")

        insertData = {
            'name' : department.Name,
            'description' : department.Description,
        }

        self.dbConnection.instance.execute_query(insertSql, insertData)

    def updateDepartment(self, department = None):
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

        self.dbConnection.instance.execute_query(updateSql, updateData)

    def deleteById(self, id = None):
        if not id:
            return
        deleteByIdSql = "DELETE FROM Department WHERE Id = {}".format(id)
        self.dbConnection.instance.execute_query(deleteByIdSql)

    def deleteByName(self, name = None):
        if not name:
            return
        deleteByNameSql = "DELETE FROM Department WHERE Name = {}".format(name)
        self.dbConnection.instance.execute_query(deleteByNameSql)

    def deleteByDepartment(self, department = None):
        if not department:
            return
        deleteById(department.Id)

    def getDepartmentById(self, id):
        selectByIdSql = "SELECT * FROM Department WHERE Id = {}".format(id)

        resultSet = self.dbConnection.instance.query_single_result(selectByIdSql)
        department = DepartmentDO.toObj(resultSet)
        return department

    @classmethod
    def getAll(self, limit = 0):
        pass

departmentDAO = DepartmentDAO()