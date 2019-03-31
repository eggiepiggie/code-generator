# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   PurchaseItemListDAO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.152754
# ===================================================================
from app.dao.Base import BaseDAO
from app.do.PurchaseItemList import PurchaseItemListDO


class PurchaseItemListDAO( BaseDAO ):
    '''Used for accessing datastore for PurchaseItemList objects.'''

    def __init__(self):
        super(PurchaseItemListDAO, self).__init__('PurchaseItemListDAO')

    def insertPurchaseItemList(self, purchaseItemList = None):
        '''Persists purchaseItemList to the database.'''
        if not purchaseItemList:
            return

        insertSql = ("INSERT INTO PurchaseItemList "
            "(PurchaseId, ItemId, Count) "
            "VALUES (%(purchaseId)s, %(itemId)s, %(count)s)")

        insertData = {
            'purchaseId' : purchaseItemList.PurchaseId,
            'itemId' : purchaseItemList.ItemId,
            'count' : purchaseItemList.Count,
        }

        purchaseItemList.Id = self.dbConnection.instance.insert_one(insertSql, insertData)
        return purchaseItemList

    def updatePurchaseItemList(self, purchaseItemList = None):
        '''Updates and persists purchaseItemList to the database.'''
        if not purchaseItemList:
            return

        updateSql = ("UPDATE PurchaseItemList "
            "SET PurchaseId = %(purchaseId)s, ItemId = %(itemId)s, Count = %(count)s"
            "WHERE Id = %(id)s")

        updateData = {
            'id' : purchaseItemList.Id,
            'purchaseId' : purchaseItemList.PurchaseId,
            'itemId' : purchaseItemList.ItemId,
            'count' : purchaseItemList.Count,
        }

        purchaseItemList.Id = self.dbConnection.instance.update_one(updateSql, updateData)
        return purchaseItemList

    def deleteById(self, id = None):
        '''Deletes purchaseItemList object from the database by id.'''
        if not id:
            return
        deleteByIdSql = "DELETE FROM PurchaseItemList WHERE Id = {}".format(id)
        return self.dbConnection.instance.execute_query(deleteByIdSql)

    def deleteByPurchaseItemList(self, purchaseItemList = None):
        '''Deletes purchaseItemList to the database.'''
        if not purchaseItemList:
            return
        return self.deleteById(purchaseItemList.Id)

    def getAllPurchaseItemLists(self, limit = None):
        '''Returns all purchaseItemLists.'''
        selectSql = "SELECT * FROM PurchaseItemList"

        resultSet = self.dbConnection.instance.query_all_result(selectSql)
        objList = []
        for row in resultSet:
            purchaseItemList = PurchaseItemListDO.toObj(row)
            objList.append(purchaseItemList)
        return objList

    def getPurchaseItemListById(self, id):
        '''Retrieves purchaseItemList by id from the database.'''
        selectByIdSql = "SELECT * FROM PurchaseItemList WHERE Id = {}".format(id)

        resultSet = self.dbConnection.instance.query_single_result(selectByIdSql)
        purchaseItemList = PurchaseItemListDO.toObj(resultSet)
        return purchaseItemList

    def getPurchaseItemListsForPurchase(self, purchase):
        '''Returns all the purchaseItemLists belonging to provided purchase.'''
        selectSql = "SELECT * FROM PurchaseItemList WHERE PurchaseId = {}".format(purchase.Id)

        resultSet = self.dbConnection.instance.query_all_result(selectSql)
        objList = []
        for row in resultSet:
            purchaseItemList = PurchaseItemListDO.toObj(row)
            objList.append(purchaseItemList)
        return objList

    def getPurchaseItemListsForItem(self, item):
        '''Returns all the purchaseItemLists belonging to provided item.'''
        selectSql = "SELECT * FROM PurchaseItemList WHERE ItemId = {}".format(item.Id)

        resultSet = self.dbConnection.instance.query_all_result(selectSql)
        objList = []
        for row in resultSet:
            purchaseItemList = PurchaseItemListDO.toObj(row)
            objList.append(purchaseItemList)
        return objList


purchaseItemListDAO = PurchaseItemListDAO()
