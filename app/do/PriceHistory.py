# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   PriceHistoryDO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.165734
# ===================================================================
from app.do.Base import BaseDO


class PriceHistoryDO( BaseDO ):
    def __init__(self, id = None, date = None, price = None, itemId = None):
        self.Id = id
        self.Date = date
        self.Price = price
        self.ItemId = itemId

    def toJson(self, simple = False):
        '''Converts this object into a json.'''
        objJson = {}
        if simple:
            objJson['Id'] = self.Id
        else:
            objJson['Id'] = self.Id
            objJson['Date'] = str(self.Date)
            objJson['Price'] = self.Price
            objJson['ItemId'] = self.ItemId
        return objJson

    def toString(self):
        '''Generates a string representation of this object.'''
        return "PriceHistoryDO[id={}, date={}, price={}, itemId={}]".format(self.Id, self.Date, self.Price, self.ItemId)

    def equalsTo(self, priceHistory):
        '''Compares this object with another object to see if they are equal.'''
        if self.Date != priceHistory.Date:
            return False
        if self.Price != priceHistory.Price:
            return False
        if self.ItemId != priceHistory.ItemId:
            return False
        return True

    @classmethod
    def toObj(self, objJson = {}):
        '''Converts json into a object.'''
        priceHistory = PriceHistoryDO()
        priceHistory.Id = objJson['Id'] if 'Id' in objJson else None
        priceHistory.Date = objJson['Date'] if 'Date' in objJson else None
        priceHistory.Price = objJson['Price'] if 'Price' in objJson else None
        priceHistory.ItemId = objJson['ItemId'] if 'ItemId' in objJson else None
        return priceHistory

