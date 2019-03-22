from app.do.Base import BaseDO

from utils.DatabaseConnection import DatabaseConnection

class FruitDO( BaseDO ):

	def __init__(self, name = None, size = None, colour = None, weight = None):
		super(FruitDO, self).__init__("FruitDO")
		self.name = name
		self.size = size
		self.colour = colour
		self.weight = weight

	def toJson(self):
		'''Method to convert class instance to json.'''
		fruit_json = {}
		fruit_json["name"] = self.name
		fruit_json["size"] = self.size
		fruit_json["colour"] = self.colour
		fruit_json["weight"] = self.weight
		return fruit_json

	def toString(self):
		'''Method to return string representation of object.'''
		params = "name='{}', size='{}', colour='{}', weight={}".format(self.name, self.size, self.colour, self.weight)
		strObject = "{}[{}]".format(self.class_name, params)
		return strObject

	def equalsTo(self, obj):
		'''Compares current object with another object.'''
		if self.name != obj.name:
			return False
		if self.size != obj.size:
			return False
		if self.colour != obj.colour:
			return False
		if self.weight != obj.weight:
			return False
		return True

	@classmethod
	def toObj(cls, obj_json):
		'''Method to convert json to class instance.'''
		name = obj_json["name"]
		size = obj_json["size"]
		colour = obj_json["colour"]
		weight = obj_json["weight"]
		return FruitDO(name, size, colour, weight)