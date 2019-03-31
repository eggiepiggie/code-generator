# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   ItemDAO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.125420
# ===================================================================
from app.dao.Base import BaseDAO
from app.do.Item import ItemDO


class ItemDAO( BaseDAO ):
    '''Used for accessing datastore for Item objects.'''

    def __init__(self):
        super(ItemDAO, self).__init__('ItemDAO')

    def insertItem(self, item = None):
        '''Persists item to the database.'''
        if not item:
            return

        insertSql = ("INSERT INTO Item "
            "(Name, Description, Colour, Weight, IsStocked, DepartmentId) "
            "VALUES (%(name)s, %(description)s, %(colour)s, %(weight)s, %(isStocked)s, %(departmentId)s)")

        insertData = {
            'name' : item.Name,
            'description' : item.Description,
            'colour' : item.Colour,
            'weight' : item.Weight,
            'isStocked' : item.IsStocked,
            'departmentId' : item.DepartmentId,
        }

        item.Id = self.dbConnection.instance.insert_one(insertSql, insertData)
        return item

    def updateItem(self, item = None):
        '''Updates and persists item to the database.'''
        if not item:
            return

        updateSql = ("UPDATE Item "
            "SET Name = %(name)s, Description = %(description)s, Colour = %(colour)s, Weight = %(weight)s, IsStocked = %(isStocked)s, DepartmentId = %(departmentId)s"
            "WHERE Id = %(id)s")

        updateData = {
            'id' : item.Id,
            'name' : item.Name,
            'description' : item.Description,
            'colour' : item.Colour,
            'weight' : item.Weight,
            'isStocked' : item.IsStocked,
            'departmentId' : item.DepartmentId,
        }

        item.Id = self.dbConnection.instance.update_one(updateSql, updateData)
        return item

    def deleteById(self, id = None):
        '''Deletes item object from the database by id.'''
        if not id:
            return
        deleteByIdSql = "DELETE FROM Item WHERE Id = {}".format(id)
        return self.dbConnection.instance.execute_query(deleteByIdSql)

    def deleteByName(self, name = None):
        '''Deletes item object from the database by name.'''
        if not name:
            return
        deleteByNameSql = "DELETE FROM Item WHERE Name = '{}'".format(name)
        return self.dbConnection.instance.execute_query(deleteByNameSql)

    def deleteByItem(self, item = None):
        '''Deletes item to the database.'''
        if not item:
            return
        return self.deleteById(item.Id)

    def getAllItems(self, limit = None):
        '''Returns all items.'''
        selectSql = "SELECT * FROM Item"

        resultSet = self.dbConnection.instance.query_all_result(selectSql)
        objList = []
        for row in resultSet:
            item = ItemDO.toObj(row)
            objList.append(item)
        return objList

    def getItemById(self, id):
        '''Retrieves item by id from the database.'''
        selectByIdSql = "SELECT * FROM Item WHERE Id = {}".format(id)

        resultSet = self.dbConnection.instance.query_single_result(selectByIdSql)
        item = ItemDO.toObj(resultSet)
        return item

    def getItemByName(self, name):
        '''Retrieves item by name from the database.'''
        selectByNameSql = "SELECT * FROM Item WHERE Name = '{}'".format(name)

        resultSet = self.dbConnection.instance.query_single_result(selectByNameSql)
        item = ItemDO.toObj(resultSet)
        return item

    def getItemsForDepartment(self, department):
        '''Returns all the items belonging to provided department.'''
        selectSql = "SELECT * FROM Item WHERE DepartmentId = {}".format(department.Id)

        resultSet = self.dbConnection.instance.query_all_result(selectSql)
        objList = []
        for row in resultSet:
            item = ItemDO.toObj(row)
            objList.append(item)
        return objList


itemDAO = ItemDAO()
