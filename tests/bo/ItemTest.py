#from app.bo.Department import DepartmentBO
#from app.bo.Item import ItemBO
from tests.extensions import TestExtension

import unittest
import datetime

# Execute this from root project folder: python -m unittest -v tests.do.FruitTest
class ItemTest( unittest.TestCase ):

	def test1(self):
		# Create department.
		department = TestExtension.createDepartmentBO("Fruit", "Sweet and yummy!")
		self.assertIsNotNone(department.department.Id)

		# # Create item called Apple.
		item = TestExtension.createItemBO("Apple", "Sweet and crisp!", 0.150, True, "Red", department)
		self.assertIsNotNone(item.item.Id)

		stockLevel = TestExtension.createStockLevelBO(10, datetime.datetime.now().strftime("%Y-%m-%d"), item)
		self.assertIsNotNone(stockLevel.stockLevel)
		print(stockLevel.stockLevel.toString())

		stockLevel2 = TestExtension.createStockLevelBO(10, datetime.datetime.now().strftime("%Y-%m-%d"), item)
		self.assertIsNotNone(stockLevel2.stockLevel)
		print(stockLevel2.stockLevel.toString())

		stockLevel.delete()
		stockLevel2.delete()

		# Delete apple item first.
		item.delete()

		# Delete department.
		department.delete()

if __name__ == '__main__':
	unittest.main()