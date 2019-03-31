# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   ItemBO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.127854
# ===================================================================
from app.bo.Base import BaseBO
from app.do.Item import ItemDO

from app.dao.Item import itemDAO
from app.dao.PriceHistory import priceHistoryDAO
from app.dao.StockLevel import stockLevelDAO
from app.dao.Department import departmentDAO
from app.do.Department import DepartmentDO
from app.dao.PurchaseItemList import purchaseItemListDAO


class ItemBO( BaseBO ):
    '''Used for representing a business object item.'''

    def __init__(self, item = None):
        '''Must accept a valid ItemDO object.'''
        super(ItemBO, self).__init__('ItemBO')
        self.item = item if item else ItemDO()
        self.department = departmentDAO.getDepartmentById(item.DepartmentId) if item else DepartmentDO()

    # ==================================
    #  Property Functions
    # ==================================
    def getId(self):
        return self.item.Id

    def getName(self):
        return self.item.Name

    def setName(self, name):
        self.item.Name = name

    def getDescription(self):
        return self.item.Description

    def setDescription(self, description):
        self.item.Description = description

    def getColour(self):
        return self.item.Colour

    def setColour(self, colour):
        self.item.Colour = colour

    def getWeight(self):
        return self.item.Weight

    def setWeight(self, weight):
        self.item.Weight = weight

    def getIsStocked(self):
        return self.item.IsStocked

    def setIsStocked(self, isStocked):
        self.item.IsStocked = isStocked

    def getDepartmentId(self):
        return self.item.DepartmentId

    def setDepartmentId(self, departmentId):
        self.item.DepartmentId = departmentId

    # ==================================
    #  CRUD Functions
    # ==================================
    def save(self):
        self.item = itemDAO.insertItem(self.item)
        return self.item

    def update(self):
        self.item = itemDAO.updateItem(self.item)
        return self.item

    def delete(self):
        return itemDAO.deleteByItem(self.item)

    # ==================================
    #  PriceHistory List Functions
    # ==================================
    def getPriceHistorys(self):
        '''Returns priceHistorys belonging to this item.'''
        self.priceHistorys = priceHistoryDAO.getPriceHistorysForItem(self.item)
        return self.priceHistorys

    def addPriceHistory(self, priceHistory):
        priceHistory.ItemId = self.item.Id
        priceHistory = priceHistoryDAO.updatePriceHistory(priceHistory)
        self.priceHistorys.append(priceHistory)

    def removePriceHistory(self, priceHistory):
        '''TODO: This method can probably be removed.'''
        self.priceHistorys = self.priceHistorys.remove(priceHistory)
        priceHistoryDAO.deleteByPriceHistory(priceHistory)

    # ==================================
    #  StockLevel List Functions
    # ==================================
    def getStockLevels(self):
        '''Returns stockLevels belonging to this item.'''
        self.stockLevels = stockLevelDAO.getStockLevelsForItem(self.item)
        return self.stockLevels

    def addStockLevel(self, stockLevel):
        stockLevel.ItemId = self.item.Id
        stockLevel = stockLevelDAO.updateStockLevel(stockLevel)
        self.stockLevels.append(stockLevel)

    def removeStockLevel(self, stockLevel):
        '''TODO: This method can probably be removed.'''
        self.stockLevels = self.stockLevels.remove(stockLevel)
        stockLevelDAO.deleteByStockLevel(stockLevel)

    # ==================================
    #  PurchaseItemList List Functions
    # ==================================
    def getPurchaseItemLists(self):
        '''Returns purchaseItemLists belonging to this item.'''
        self.purchaseItemLists = purchaseItemListDAO.getPurchaseItemListsForItem(self.item)
        return self.purchaseItemLists

    def addPurchaseItemList(self, purchaseItemList):
        purchaseItemList.ItemId = self.item.Id
        purchaseItemList = purchaseItemListDAO.updatePurchaseItemList(purchaseItemList)
        self.purchaseItemLists.append(purchaseItemList)

    def removePurchaseItemList(self, purchaseItemList):
        '''TODO: This method can probably be removed.'''
        self.purchaseItemLists = self.purchaseItemLists.remove(purchaseItemList)
        purchaseItemListDAO.deleteByPurchaseItemList(purchaseItemList)

