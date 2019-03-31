# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   PurchaseItemListDO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.149933
# ===================================================================
from app.do.Base import BaseDO


class PurchaseItemListDO( BaseDO ):
    def __init__(self, id = None, purchaseId = None, itemId = None, count = None):
        self.Id = id
        self.PurchaseId = purchaseId
        self.ItemId = itemId
        self.Count = count

    def toJson(self, simple = False):
        '''Converts this object into a json.'''
        objJson = {}
        if simple:
            objJson['Id'] = self.Id
        else:
            objJson['Id'] = self.Id
            objJson['PurchaseId'] = self.PurchaseId
            objJson['ItemId'] = self.ItemId
            objJson['Count'] = self.Count
        return objJson

    def toString(self):
        '''Generates a string representation of this object.'''
        return "PurchaseItemListDO[id={}, purchaseId={}, itemId={}, count={}]".format(self.Id, self.PurchaseId, self.ItemId, self.Count)

    def equalsTo(self, purchaseItemList):
        '''Compares this object with another object to see if they are equal.'''
        if self.PurchaseId != purchaseItemList.PurchaseId:
            return False
        if self.ItemId != purchaseItemList.ItemId:
            return False
        if self.Count != purchaseItemList.Count:
            return False
        return True

    @classmethod
    def toObj(self, objJson = {}):
        '''Converts json into a object.'''
        purchaseItemList = PurchaseItemListDO()
        purchaseItemList.Id = objJson['Id'] if 'Id' in objJson else None
        purchaseItemList.PurchaseId = objJson['PurchaseId'] if 'PurchaseId' in objJson else None
        purchaseItemList.ItemId = objJson['ItemId'] if 'ItemId' in objJson else None
        purchaseItemList.Count = objJson['Count'] if 'Count' in objJson else None
        return purchaseItemList

