from app.do.Department import DepartmentDO
from app.do.Item import ItemDO
from app.dao.Department import departmentDAO
from app.dao.Item import itemDAO

import unittest

# Execute this from root project folder: python -m unittest -v tests.do.FruitTest
class ItemTest( unittest.TestCase ):

	conn = departmentDAO.dbConnection.instance
	d = None

	def test1DatabaseConnection(self):
		self.assertTrue(self.conn.query_table_exists("Item"))

	def test2FirstInsert(self):
		self.d = DepartmentDO()
		self.d.Name = "Fruit"
		self.d.Description = "Sweet and yummy!"
		self.d = departmentDAO.insertDepartment(self.d)
		self.assertIsNotNone(self.d.Id)

	def test3SecondInsert(self):
		department = departmentDAO.getDepartmentByName("Fruit")

		item = ItemDO()
		item.Name = "Apple"
		item.Description = "Sweet but Crisp!"
		item.Colour = "Red"
		item.Weight = 0.150
		item.IsStocked = True
		item.DepartmentId = department.Id
		item = itemDAO.insertItem(item)
		self.assertIsNotNone(item.Id)

	def test4FirstDelete(self):
		rowsAffected = itemDAO.deleteByName("Apple")
		self.assertEqual(1, rowsAffected)

	def test5SecondDelete(self):
		rowsAffected = departmentDAO.deleteByName("Fruit")
		self.assertEqual(1, rowsAffected)

if __name__ == '__main__':
	unittest.main()