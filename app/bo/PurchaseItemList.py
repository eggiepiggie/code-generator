# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   PurchaseItemListBO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.154872
# ===================================================================
from app.bo.Base import BaseBO
from app.do.PurchaseItemList import PurchaseItemListDO

from app.dao.PurchaseItemList import purchaseItemListDAO
from app.dao.Purchase import purchaseDAO
from app.do.Purchase import PurchaseDO
from app.dao.Item import itemDAO
from app.do.Item import ItemDO


class PurchaseItemListBO( BaseBO ):
    '''Used for representing a business object purchaseItemList.'''

    def __init__(self, purchaseItemList = None):
        '''Must accept a valid PurchaseItemListDO object.'''
        super(PurchaseItemListBO, self).__init__('PurchaseItemListBO')
        self.purchaseItemList = purchaseItemList if purchaseItemList else PurchaseItemListDO()
        self.purchase = purchaseDAO.getPurchaseById(purchaseItemList.PurchaseId) if purchaseItemList else PurchaseDO()
        self.item = itemDAO.getItemById(purchaseItemList.ItemId) if purchaseItemList else ItemDO()

    # ==================================
    #  Property Functions
    # ==================================
    def getId(self):
        return self.purchaseItemList.Id

    def getPurchaseId(self):
        return self.purchaseItemList.PurchaseId

    def setPurchaseId(self, purchaseId):
        self.purchaseItemList.PurchaseId = purchaseId

    def getItemId(self):
        return self.purchaseItemList.ItemId

    def setItemId(self, itemId):
        self.purchaseItemList.ItemId = itemId

    def getCount(self):
        return self.purchaseItemList.Count

    def setCount(self, count):
        self.purchaseItemList.Count = count

    # ==================================
    #  CRUD Functions
    # ==================================
    def save(self):
        self.purchaseItemList = purchaseItemListDAO.insertPurchaseItemList(self.purchaseItemList)
        return self.purchaseItemList

    def update(self):
        self.purchaseItemList = purchaseItemListDAO.updatePurchaseItemList(self.purchaseItemList)
        return self.purchaseItemList

    def delete(self):
        return purchaseItemListDAO.deleteByPurchaseItemList(self.purchaseItemList)

