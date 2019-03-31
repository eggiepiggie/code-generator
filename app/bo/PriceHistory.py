# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   PriceHistoryBO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.169373
# ===================================================================
from app.bo.Base import BaseBO
from app.do.PriceHistory import PriceHistoryDO

from app.dao.PriceHistory import priceHistoryDAO
from app.dao.Item import itemDAO
from app.do.Item import ItemDO


class PriceHistoryBO( BaseBO ):
    '''Used for representing a business object priceHistory.'''

    def __init__(self, priceHistory = None):
        '''Must accept a valid PriceHistoryDO object.'''
        super(PriceHistoryBO, self).__init__('PriceHistoryBO')
        self.priceHistory = priceHistory if priceHistory else PriceHistoryDO()
        self.item = itemDAO.getItemById(priceHistory.ItemId) if priceHistory else ItemDO()

    # ==================================
    #  Property Functions
    # ==================================
    def getId(self):
        return self.priceHistory.Id

    def getDate(self):
        return self.priceHistory.Date

    def setDate(self, date):
        self.priceHistory.Date = date

    def getPrice(self):
        return self.priceHistory.Price

    def setPrice(self, price):
        self.priceHistory.Price = price

    def getItemId(self):
        return self.priceHistory.ItemId

    def setItemId(self, itemId):
        self.priceHistory.ItemId = itemId

    # ==================================
    #  CRUD Functions
    # ==================================
    def save(self):
        self.priceHistory = priceHistoryDAO.insertPriceHistory(self.priceHistory)
        return self.priceHistory

    def update(self):
        self.priceHistory = priceHistoryDAO.updatePriceHistory(self.priceHistory)
        return self.priceHistory

    def delete(self):
        return priceHistoryDAO.deleteByPriceHistory(self.priceHistory)

