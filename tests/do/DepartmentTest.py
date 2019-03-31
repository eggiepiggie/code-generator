from app.do.Department import DepartmentDO
from app.dao.Department import departmentDAO

import unittest

# Execute this from root project folder: python -m unittest -v tests.do.FruitTest
class DepartmentTest( unittest.TestCase ):

	conn = departmentDAO.dbConnection.instance

	def test1DatabaseConnection(self):
		self.assertTrue(self.conn.query_table_exists("Department"))

	def test2FirstInsert(self):
		d = DepartmentDO()
		d.Name = "Fruit"
		d.Description = "Sweet and yummy!"
		d = departmentDAO.insertDepartment(d)
		self.assertIsNotNone(d.Id)

	def test3SecondInsert(self):
		d = DepartmentDO()
		d.Name = "Meat"
		d.Description = "Meaty-or!"
		d = departmentDAO.insertDepartment(d)
		self.assertIsNotNone(d.Id)

	def test4GetAll(self):
		result = departmentDAO.getAllDepartments()
		self.assertEqual(2, len(result))

	def test5GetByName(self):
		result = departmentDAO.getDepartmentByName("Fruit")
		self.assertEqual("Fruit", result.Name)

	def test6FirstDelete(self):
		result = departmentDAO.getDepartmentByName("Meat")
		rowsAffected = departmentDAO.deleteById(result.Id)
		self.assertEqual(1, rowsAffected)

	def test7FirstUpdate(self):
		result = departmentDAO.getDepartmentByName("Fruit")
		result.Description = "Perfection"
		result = departmentDAO.updateDepartment(result)
		self.assertIsNotNone(result.Id)

	def test8SecondDelete(self):
		rowsAffected = departmentDAO.deleteByName("Fruit")
		self.assertEqual(1, rowsAffected)


if __name__ == '__main__':
	unittest.main(sortTestMethodsUsing = None)