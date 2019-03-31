# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   PurchaseDO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.135422
# ===================================================================
from app.do.Base import BaseDO


class PurchaseDO( BaseDO ):
    def __init__(self, id = None, customer = None, purchaseDate = None):
        self.Id = id
        self.Customer = customer
        self.PurchaseDate = purchaseDate

    def toJson(self, simple = False):
        '''Converts this object into a json.'''
        objJson = {}
        if simple:
            objJson['Id'] = self.Id
        else:
            objJson['Id'] = self.Id
            objJson['Customer'] = self.Customer
            objJson['PurchaseDate'] = str(self.PurchaseDate)
        return objJson

    def toString(self):
        '''Generates a string representation of this object.'''
        return "PurchaseDO[id={}, customer={}, purchaseDate={}]".format(self.Id, self.Customer, self.PurchaseDate)

    def equalsTo(self, purchase):
        '''Compares this object with another object to see if they are equal.'''
        if self.Customer != purchase.Customer:
            return False
        if self.PurchaseDate != purchase.PurchaseDate:
            return False
        return True

    @classmethod
    def toObj(self, objJson = {}):
        '''Converts json into a object.'''
        purchase = PurchaseDO()
        purchase.Id = objJson['Id'] if 'Id' in objJson else None
        purchase.Customer = objJson['Customer'] if 'Customer' in objJson else None
        purchase.PurchaseDate = objJson['PurchaseDate'] if 'PurchaseDate' in objJson else None
        return purchase

