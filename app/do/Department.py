# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   DepartmentDO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.109141
# ===================================================================
from app.do.Base import BaseDO


class DepartmentDO( BaseDO ):
    def __init__(self, id = None, name = None, description = None):
        self.Id = id
        self.Name = name
        self.Description = description

    def toJson(self, simple = False):
        '''Converts this object into a json.'''
        objJson = {}
        if simple:
            objJson['Id'] = self.Id
        else:
            objJson['Id'] = self.Id
            objJson['Name'] = self.Name
            objJson['Description'] = self.Description
        return objJson

    def toString(self):
        '''Generates a string representation of this object.'''
        return "DepartmentDO[id={}, name={}, description={}]".format(self.Id, self.Name, self.Description)

    def equalsTo(self, department):
        '''Compares this object with another object to see if they are equal.'''
        if self.Name != department.Name:
            return False
        if self.Description != department.Description:
            return False
        return True

    @classmethod
    def toObj(self, objJson = {}):
        '''Converts json into a object.'''
        department = DepartmentDO()
        department.Id = objJson['Id'] if 'Id' in objJson else None
        department.Name = objJson['Name'] if 'Name' in objJson else None
        department.Description = objJson['Description'] if 'Description' in objJson else None
        return department

