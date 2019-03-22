from app.do.Department import DepartmentDO
from app.dao.Department import departmentDAO

import unittest

# Execute this from root project folder: python -m unittest -v tests.do.FruitTest
class DepartmentTest( unittest.TestCase ):

	conn = departmentDAO.dbConnection.instance

	def testDatabaseConnection(self):
		self.assertTrue(self.conn.query_table_exists("Department"))

	def testInsert(self):
		d = DepartmentDO()
		d.Id = 1
		d.Name = "Fruit"
		d.Description = "Sweet and yummy!"
		departmentDAO.insertDepartment(d)
		self.assertEqual(1, self.conn.count_entries("Department"))

	def testDelete(self):
		departmentDAO.deleteById(7)
		self.assertEqual(0, self.conn.count_entries("Department"))

if __name__ == '__main__':
	unittest.main()