# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   StockLevelDAO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.160275
# ===================================================================
from app.dao.Base import BaseDAO
from app.do.StockLevel import StockLevelDO


class StockLevelDAO( BaseDAO ):
    '''Used for accessing datastore for StockLevel objects.'''

    def __init__(self):
        super(StockLevelDAO, self).__init__('StockLevelDAO')

    def insertStockLevel(self, stockLevel = None):
        '''Persists stockLevel to the database.'''
        if not stockLevel:
            return

        insertSql = ("INSERT INTO StockLevel "
            "(ItemId, Count, NextShipment) "
            "VALUES (%(itemId)s, %(count)s, %(nextShipment)s)")

        insertData = {
            'itemId' : stockLevel.ItemId,
            'count' : stockLevel.Count,
            'nextShipment' : stockLevel.NextShipment,
        }

        stockLevel.Id = self.dbConnection.instance.insert_one(insertSql, insertData)
        return stockLevel

    def updateStockLevel(self, stockLevel = None):
        '''Updates and persists stockLevel to the database.'''
        if not stockLevel:
            return

        updateSql = ("UPDATE StockLevel "
            "SET ItemId = %(itemId)s, Count = %(count)s, NextShipment = %(nextShipment)s"
            "WHERE Id = %(id)s")

        updateData = {
            'id' : stockLevel.Id,
            'itemId' : stockLevel.ItemId,
            'count' : stockLevel.Count,
            'nextShipment' : stockLevel.NextShipment,
        }

        stockLevel.Id = self.dbConnection.instance.update_one(updateSql, updateData)
        return stockLevel

    def deleteById(self, id = None):
        '''Deletes stockLevel object from the database by id.'''
        if not id:
            return
        deleteByIdSql = "DELETE FROM StockLevel WHERE Id = {}".format(id)
        return self.dbConnection.instance.execute_query(deleteByIdSql)

    def deleteByItemId(self, itemId = None):
        '''Deletes stockLevel object from the database by itemId.'''
        if not itemId:
            return
        deleteByItemIdSql = "DELETE FROM StockLevel WHERE ItemId = {}".format(itemId)
        return self.dbConnection.instance.execute_query(deleteByItemIdSql)

    def deleteByStockLevel(self, stockLevel = None):
        '''Deletes stockLevel to the database.'''
        if not stockLevel:
            return
        return self.deleteById(stockLevel.Id)

    def getAllStockLevels(self, limit = None):
        '''Returns all stockLevels.'''
        selectSql = "SELECT * FROM StockLevel"

        resultSet = self.dbConnection.instance.query_all_result(selectSql)
        objList = []
        for row in resultSet:
            stockLevel = StockLevelDO.toObj(row)
            objList.append(stockLevel)
        return objList

    def getStockLevelById(self, id):
        '''Retrieves stockLevel by id from the database.'''
        selectByIdSql = "SELECT * FROM StockLevel WHERE Id = {}".format(id)

        resultSet = self.dbConnection.instance.query_single_result(selectByIdSql)
        stockLevel = StockLevelDO.toObj(resultSet)
        return stockLevel

    def getStockLevelByItemId(self, itemId):
        '''Retrieves stockLevel by itemId from the database.'''
        selectByItemIdSql = "SELECT * FROM StockLevel WHERE ItemId = {}".format(itemId)

        resultSet = self.dbConnection.instance.query_single_result(selectByItemIdSql)
        stockLevel = StockLevelDO.toObj(resultSet)
        return stockLevel

    def getStockLevelsForItem(self, item):
        '''Returns all the stockLevels belonging to provided item.'''
        selectSql = "SELECT * FROM StockLevel WHERE ItemId = {}".format(item.Id)

        resultSet = self.dbConnection.instance.query_all_result(selectSql)
        objList = []
        for row in resultSet:
            stockLevel = StockLevelDO.toObj(row)
            objList.append(stockLevel)
        return objList


stockLevelDAO = StockLevelDAO()
