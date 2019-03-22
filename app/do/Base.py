class BaseDO(object):
	'''Parent Base DO class.'''

	def __init__(self, class_name = "BaseDO"):
		self.class_name = class_name

	def toJson(self):
		'''Method to convert class instance to json.'''
		pass

	def toString(self):
		'''Method to return string representation of object.'''
		pass

	def equalsTo(self, obj):
		'''Compares current object with another object.'''
		pass

	@classmethod
	def toObj(cls, obj_json):
		'''Method to convert json to class instance.'''
		pass