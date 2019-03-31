# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   StockLevelBO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.162048
# ===================================================================
from app.bo.Base import BaseBO
from app.do.StockLevel import StockLevelDO

from app.dao.StockLevel import stockLevelDAO
from app.dao.Item import itemDAO
from app.do.Item import ItemDO


class StockLevelBO( BaseBO ):
    '''Used for representing a business object stockLevel.'''

    def __init__(self, stockLevel = None):
        '''Must accept a valid StockLevelDO object.'''
        super(StockLevelBO, self).__init__('StockLevelBO')
        self.stockLevel = stockLevel if stockLevel else StockLevelDO()
        self.item = itemDAO.getItemById(stockLevel.ItemId) if stockLevel else ItemDO()

    # ==================================
    #  Property Functions
    # ==================================
    def getId(self):
        return self.stockLevel.Id

    def getItemId(self):
        return self.stockLevel.ItemId

    def setItemId(self, itemId):
        self.stockLevel.ItemId = itemId

    def getCount(self):
        return self.stockLevel.Count

    def setCount(self, count):
        self.stockLevel.Count = count

    def getNextShipment(self):
        return self.stockLevel.NextShipment

    def setNextShipment(self, nextShipment):
        self.stockLevel.NextShipment = nextShipment

    # ==================================
    #  CRUD Functions
    # ==================================
    def save(self):
        self.stockLevel = stockLevelDAO.insertStockLevel(self.stockLevel)
        return self.stockLevel

    def update(self):
        self.stockLevel = stockLevelDAO.updateStockLevel(self.stockLevel)
        return self.stockLevel

    def delete(self):
        return stockLevelDAO.deleteByStockLevel(self.stockLevel)

