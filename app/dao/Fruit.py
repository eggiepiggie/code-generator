from app.dao.Base import BaseDAO

class FruitDAO( BaseDAO ):

	def __init__(self):
		super(FruitDAO, self).__init__("FruitDAO")

	def getById(self, id):
		pass

	@classmethod
	def getAll(self, limit = 0):
		pass

fruitDAO = FruitDAO()