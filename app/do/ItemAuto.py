# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   ItemDO Class
#
# ===================================================================
#  Generated on: 2019-03-24 16:55:47.514869
# ===================================================================
from app.do.Base import BaseDO


class ItemDO( BaseDO ):
    def __init__(self, id = None, name = None, description = None, colour = None, weight = None, isStocked = None, departmentId = None):
        self.Id = id
        self.Name = name
        self.Description = description
        self.Colour = colour
        self.Weight = weight
        self.IsStocked = isStocked
        self.DepartmentId = departmentId

    def toJson(self, simple = False):
        '''Converts this object into a json.'''
        objJson = {}
        if simple:
            objJson['Id'] = self.Id
        else:
            objJson['Id'] = self.Id
            objJson['Name'] = self.Name
            objJson['Description'] = self.Description
            objJson['Colour'] = self.Colour
            objJson['Weight'] = self.Weight
            objJson['IsStocked'] = self.IsStocked
            objJson['DepartmentId'] = self.DepartmentId
        return objJson

    def toString(self):
        '''Generates a string representation of this object.'''
        return "ItemDO[id={}, name={}, description={}, colour={}, weight={}, isStocked={}, departmentId={}]".format(self.Id, self.Name, self.Description, self.Colour, self.Weight, self.IsStocked, self.DepartmentId)

    def equalsTo(self, item):
        '''Compares this object with another object to see if they are equal.'''
        if self.Name != item.Name:
            return False
        if self.Description != item.Description:
            return False
        if self.Colour != item.Colour:
            return False
        if self.Weight != item.Weight:
            return False
        if self.IsStocked != item.IsStocked:
            return False
        if self.DepartmentId != item.DepartmentId:
            return False
        return True

    @classmethod
    def toObj(self, objJson = {}):
        '''Converts json into a object.'''
        item = Item()
        item.Id = objJson['Id'] if 'Id' in objJson else None
        item.Name = objJson['Name'] if 'Name' in objJson else None
        item.Description = objJson['Description'] if 'Description' in objJson else None
        item.Colour = objJson['Colour'] if 'Colour' in objJson else None
        item.Weight = objJson['Weight'] if 'Weight' in objJson else None
        item.IsStocked = objJson['IsStocked'] if 'IsStocked' in objJson else None
        item.DepartmentId = objJson['DepartmentId'] if 'DepartmentId' in objJson else None
        return item


