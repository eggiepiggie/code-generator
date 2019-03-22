from utils.DatabaseConnection import DatabaseConnection

import unittest

# Execute this from root project folder: python -m unittest -v tests.do.DatabaseConnectionTest
class DatabaseConnectionTest( unittest.TestCase ):

	def testCreateDatabaseConnection(self):
		db_conn = DatabaseConnection()
		self.assertIsNotNone(db_conn)
		self.assertIsNotNone(db_conn.connection)
		self.assertTrue(db_conn.connection.is_connected)
		self.assertEqual(db_conn.connection.database, "market")

if __name__ == '__main__':
	unittest.main()