from app.do.Fruit import FruitDO
from app.dao.Fruit import fruitDAO

import unittest

# Execute this from root project folder: python -m unittest -v tests.do.FruitTest
class FruitTest( unittest.TestCase ):

	def testCreateFruitInstance(self):
		apple = FruitDO("Apple", "S", "Red", 0.150)
		self.assertEqual(apple.name, "Apple")
		self.assertEqual(apple.size, "S")
		self.assertEqual(apple.colour, "Red")
		self.assertEqual(apple.weight, 0.150)
		self.assertEqual(apple.class_name, "FruitDO")

	def testToObjMethod(self):
		banana_json = {
			"name": "banana",
			"size": "S",
			"colour": "Yellow",
			"weight": 0.100
		}
		banana = FruitDO.toObj(banana_json)
		self.assertEqual(banana.name, banana_json["name"])
		self.assertEqual(banana.size, banana_json["size"])
		self.assertEqual(banana.colour, banana_json["colour"])
		self.assertEqual(banana.weight, banana_json["weight"])

	def testToJsonMethod(self):
		orange = FruitDO("Orange", "S", "Orange", 0.200)
		orange_json = orange.toJson()
		self.assertEqual(orange.name, orange_json["name"])
		self.assertEqual(orange.size, orange_json["size"])
		self.assertEqual(orange.colour, orange_json["colour"])
		self.assertEqual(orange.weight, orange_json["weight"])

	def testCompareTwoIdenticalFruits(self):
		peach1 = FruitDO("Peach", "S", "Pink", 0.100)
		peach2 = FruitDO("Peach", "S", "Pink", 0.100)
		self.assertTrue(peach1.equalsTo(peach2))

	def testCompareTwoDifferentFruits(self):
		lime = FruitDO("Lime", "S", "Green", 0.070)
		lemon = FruitDO("Lemon", "S", "Yellow", 0.070)
		self.assertFalse(lime.equalsTo(lemon))

	def testStringRepresentationOfObject(self):
		mango = FruitDO("Mango", "S", "Yellow", 0.200)
		self.assertEquals(mango.toString(), "FruitDO[name='Mango', size='S', colour='Yellow', weight=0.2]")

	def testDatabaseConnection(self):
		conn = fruitDAO.dbConnection.instance
		self.assertFalse(conn.query_table_exists("Fruit"))

if __name__ == '__main__':
	unittest.main()