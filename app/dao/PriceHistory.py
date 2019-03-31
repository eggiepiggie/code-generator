# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   PriceHistoryDAO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.167294
# ===================================================================
from app.dao.Base import BaseDAO
from app.do.PriceHistory import PriceHistoryDO


class PriceHistoryDAO( BaseDAO ):
    '''Used for accessing datastore for PriceHistory objects.'''

    def __init__(self):
        super(PriceHistoryDAO, self).__init__('PriceHistoryDAO')

    def insertPriceHistory(self, priceHistory = None):
        '''Persists priceHistory to the database.'''
        if not priceHistory:
            return

        insertSql = ("INSERT INTO PriceHistory "
            "(Date, Price, ItemId) "
            "VALUES (%(date)s, %(price)s, %(itemId)s)")

        insertData = {
            'date' : priceHistory.Date,
            'price' : priceHistory.Price,
            'itemId' : priceHistory.ItemId,
        }

        priceHistory.Id = self.dbConnection.instance.insert_one(insertSql, insertData)
        return priceHistory

    def updatePriceHistory(self, priceHistory = None):
        '''Updates and persists priceHistory to the database.'''
        if not priceHistory:
            return

        updateSql = ("UPDATE PriceHistory "
            "SET Date = %(date)s, Price = %(price)s, ItemId = %(itemId)s"
            "WHERE Id = %(id)s")

        updateData = {
            'id' : priceHistory.Id,
            'date' : priceHistory.Date,
            'price' : priceHistory.Price,
            'itemId' : priceHistory.ItemId,
        }

        priceHistory.Id = self.dbConnection.instance.update_one(updateSql, updateData)
        return priceHistory

    def deleteById(self, id = None):
        '''Deletes priceHistory object from the database by id.'''
        if not id:
            return
        deleteByIdSql = "DELETE FROM PriceHistory WHERE Id = {}".format(id)
        return self.dbConnection.instance.execute_query(deleteByIdSql)

    def deleteByPriceHistory(self, priceHistory = None):
        '''Deletes priceHistory to the database.'''
        if not priceHistory:
            return
        return self.deleteById(priceHistory.Id)

    def getAllPriceHistorys(self, limit = None):
        '''Returns all priceHistorys.'''
        selectSql = "SELECT * FROM PriceHistory"

        resultSet = self.dbConnection.instance.query_all_result(selectSql)
        objList = []
        for row in resultSet:
            priceHistory = PriceHistoryDO.toObj(row)
            objList.append(priceHistory)
        return objList

    def getPriceHistoryById(self, id):
        '''Retrieves priceHistory by id from the database.'''
        selectByIdSql = "SELECT * FROM PriceHistory WHERE Id = {}".format(id)

        resultSet = self.dbConnection.instance.query_single_result(selectByIdSql)
        priceHistory = PriceHistoryDO.toObj(resultSet)
        return priceHistory

    def getPriceHistorysForItem(self, item):
        '''Returns all the priceHistorys belonging to provided item.'''
        selectSql = "SELECT * FROM PriceHistory WHERE ItemId = {}".format(item.Id)

        resultSet = self.dbConnection.instance.query_all_result(selectSql)
        objList = []
        for row in resultSet:
            priceHistory = PriceHistoryDO.toObj(row)
            objList.append(priceHistory)
        return objList


priceHistoryDAO = PriceHistoryDAO()
