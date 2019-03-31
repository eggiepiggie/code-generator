# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   DepartmentBO Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.116795
# ===================================================================
from app.bo.Base import BaseBO
from app.do.Department import DepartmentDO

from app.dao.Department import departmentDAO
from app.dao.Item import itemDAO


class DepartmentBO( BaseBO ):
    '''Used for representing a business object department.'''

    def __init__(self, department = None):
        '''Must accept a valid DepartmentDO object.'''
        super(DepartmentBO, self).__init__('DepartmentBO')
        self.department = department if department else DepartmentDO()

    # ==================================
    #  Property Functions
    # ==================================
    def getId(self):
        return self.department.Id

    def getName(self):
        return self.department.Name

    def setName(self, name):
        self.department.Name = name

    def getDescription(self):
        return self.department.Description

    def setDescription(self, description):
        self.department.Description = description

    # ==================================
    #  CRUD Functions
    # ==================================
    def save(self):
        self.department = departmentDAO.insertDepartment(self.department)
        return self.department

    def update(self):
        self.department = departmentDAO.updateDepartment(self.department)
        return self.department

    def delete(self):
        return departmentDAO.deleteByDepartment(self.department)

    # ==================================
    #  Item List Functions
    # ==================================
    def getItems(self):
        '''Returns items belonging to this department.'''
        self.items = itemDAO.getItemsForDepartment(self.department)
        return self.items

    def addItem(self, item):
        item.DepartmentId = self.department.Id
        item = itemDAO.updateItem(item)
        self.items.append(item)

    def removeItem(self, item):
        '''TODO: This method can probably be removed.'''
        self.items = self.items.remove(item)
        itemDAO.deleteByItem(item)

