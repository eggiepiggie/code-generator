from app.do.Base import BaseDO

from utils.DatabaseConnection import DatabaseConnection

class DepartmentDO( BaseDO ):

	def __init__(self, obj_id = None, name = None, description = None):
		super(DepartmentDO, self).__init__("DepartmentDO")
		self.Id = obj_id
		self.Name = name
		self.Description = description

	def toJson(self):
		'''Method to convert class instance to json.'''
		department_json = {}
		department_json["Id"] = self.Id
		department_json["Name"] = self.Name
		department_json["Description"] = self.Description
		return department_json

	def toString(self):
		'''Method to return string representation of object.'''
		params = "name='{}', description='{}'".format(self.Name, self.Description)
		strObject = "{}[{}]".format(self.class_name, params)
		return strObject

	def equalsTo(self, obj):
		'''Compares current object with another object.'''
		if self.Name != obj.Name:
			return False
		if self.Description != obj.Description:
			return False
		return True

	@classmethod
	def toObj(cls, obj_json):
		'''Method to convert json to class instance.'''
		department = DepartmentDO()
		department.Id = obj_json["Id"]
		department.Name = obj_json["Name"]
		department.Description = obj_json["Description"]
		return department