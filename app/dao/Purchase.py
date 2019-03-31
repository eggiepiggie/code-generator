# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   PurchaseDAO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.138926
# ===================================================================
from app.dao.Base import BaseDAO
from app.do.Purchase import PurchaseDO


class PurchaseDAO( BaseDAO ):
    '''Used for accessing datastore for Purchase objects.'''

    def __init__(self):
        super(PurchaseDAO, self).__init__('PurchaseDAO')

    def insertPurchase(self, purchase = None):
        '''Persists purchase to the database.'''
        if not purchase:
            return

        insertSql = ("INSERT INTO Purchase "
            "(Customer, PurchaseDate) "
            "VALUES (%(customer)s, %(purchaseDate)s)")

        insertData = {
            'customer' : purchase.Customer,
            'purchaseDate' : purchase.PurchaseDate,
        }

        purchase.Id = self.dbConnection.instance.insert_one(insertSql, insertData)
        return purchase

    def updatePurchase(self, purchase = None):
        '''Updates and persists purchase to the database.'''
        if not purchase:
            return

        updateSql = ("UPDATE Purchase "
            "SET Customer = %(customer)s, PurchaseDate = %(purchaseDate)s"
            "WHERE Id = %(id)s")

        updateData = {
            'id' : purchase.Id,
            'customer' : purchase.Customer,
            'purchaseDate' : purchase.PurchaseDate,
        }

        purchase.Id = self.dbConnection.instance.update_one(updateSql, updateData)
        return purchase

    def deleteById(self, id = None):
        '''Deletes purchase object from the database by id.'''
        if not id:
            return
        deleteByIdSql = "DELETE FROM Purchase WHERE Id = {}".format(id)
        return self.dbConnection.instance.execute_query(deleteByIdSql)

    def deleteByPurchase(self, purchase = None):
        '''Deletes purchase to the database.'''
        if not purchase:
            return
        return self.deleteById(purchase.Id)

    def getAllPurchases(self, limit = None):
        '''Returns all purchases.'''
        selectSql = "SELECT * FROM Purchase"

        resultSet = self.dbConnection.instance.query_all_result(selectSql)
        objList = []
        for row in resultSet:
            purchase = PurchaseDO.toObj(row)
            objList.append(purchase)
        return objList

    def getPurchaseById(self, id):
        '''Retrieves purchase by id from the database.'''
        selectByIdSql = "SELECT * FROM Purchase WHERE Id = {}".format(id)

        resultSet = self.dbConnection.instance.query_single_result(selectByIdSql)
        purchase = PurchaseDO.toObj(resultSet)
        return purchase


purchaseDAO = PurchaseDAO()
