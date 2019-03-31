# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   PurchaseBO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.141331
# ===================================================================
from app.bo.Base import BaseBO
from app.do.Purchase import PurchaseDO

from app.dao.Purchase import purchaseDAO
from app.dao.PurchaseItemList import purchaseItemListDAO


class PurchaseBO( BaseBO ):
    '''Used for representing a business object purchase.'''

    def __init__(self, purchase = None):
        '''Must accept a valid PurchaseDO object.'''
        super(PurchaseBO, self).__init__('PurchaseBO')
        self.purchase = purchase if purchase else PurchaseDO()

    # ==================================
    #  Property Functions
    # ==================================
    def getId(self):
        return self.purchase.Id

    def getCustomer(self):
        return self.purchase.Customer

    def setCustomer(self, customer):
        self.purchase.Customer = customer

    def getPurchaseDate(self):
        return self.purchase.PurchaseDate

    def setPurchaseDate(self, purchaseDate):
        self.purchase.PurchaseDate = purchaseDate

    # ==================================
    #  CRUD Functions
    # ==================================
    def save(self):
        self.purchase = purchaseDAO.insertPurchase(self.purchase)
        return self.purchase

    def update(self):
        self.purchase = purchaseDAO.updatePurchase(self.purchase)
        return self.purchase

    def delete(self):
        return purchaseDAO.deleteByPurchase(self.purchase)

    # ==================================
    #  PurchaseItemList List Functions
    # ==================================
    def getPurchaseItemLists(self):
        '''Returns purchaseItemLists belonging to this purchase.'''
        self.purchaseItemLists = purchaseItemListDAO.getPurchaseItemListsForPurchase(self.purchase)
        return self.purchaseItemLists

    def addPurchaseItemList(self, purchaseItemList):
        purchaseItemList.PurchaseId = self.purchase.Id
        purchaseItemList = purchaseItemListDAO.updatePurchaseItemList(purchaseItemList)
        self.purchaseItemLists.append(purchaseItemList)

    def removePurchaseItemList(self, purchaseItemList):
        '''TODO: This method can probably be removed.'''
        self.purchaseItemLists = self.purchaseItemLists.remove(purchaseItemList)
        purchaseItemListDAO.deleteByPurchaseItemList(purchaseItemList)

