# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   StockLevelDO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.158934
# ===================================================================
from app.do.Base import BaseDO


class StockLevelDO( BaseDO ):
    def __init__(self, id = None, itemId = None, count = None, nextShipment = None):
        self.Id = id
        self.ItemId = itemId
        self.Count = count
        self.NextShipment = nextShipment

    def toJson(self, simple = False):
        '''Converts this object into a json.'''
        objJson = {}
        if simple:
            objJson['Id'] = self.Id
        else:
            objJson['Id'] = self.Id
            objJson['ItemId'] = self.ItemId
            objJson['Count'] = self.Count
            objJson['NextShipment'] = str(self.NextShipment)
        return objJson

    def toString(self):
        '''Generates a string representation of this object.'''
        return "StockLevelDO[id={}, itemId={}, count={}, nextShipment={}]".format(self.Id, self.ItemId, self.Count, self.NextShipment)

    def equalsTo(self, stockLevel):
        '''Compares this object with another object to see if they are equal.'''
        if self.ItemId != stockLevel.ItemId:
            return False
        if self.Count != stockLevel.Count:
            return False
        if self.NextShipment != stockLevel.NextShipment:
            return False
        return True

    @classmethod
    def toObj(self, objJson = {}):
        '''Converts json into a object.'''
        stockLevel = StockLevelDO()
        stockLevel.Id = objJson['Id'] if 'Id' in objJson else None
        stockLevel.ItemId = objJson['ItemId'] if 'ItemId' in objJson else None
        stockLevel.Count = objJson['Count'] if 'Count' in objJson else None
        stockLevel.NextShipment = objJson['NextShipment'] if 'NextShipment' in objJson else None
        return stockLevel

