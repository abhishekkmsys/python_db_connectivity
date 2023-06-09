import unittest
import logging
import pyodbc
import configurations.config as config
from utilities.helper_functions import load_json, setup_logging
import Database_Connection.db_connection as db_connection

class TestMsysAccounts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.input_data = load_json('TestData/input_account_data.json')
        setup_logging('logs/test_accounts.log')

    def setUp(self):
        
        try:
            # create connection
            self.connection = db_connection.create_connection()

            # create cursor object
            self.cursor = self.connection.cursor()

            # execute SQL query to retrieve data from Msys_Accounts table
            self.cursor.execute('SELECT * FROM Msys_Accounts')
            self.rows = self.cursor.fetchall()


        except pyodbc.Error as err:
            logging.error(f"Database Connectivity Failed. {err}") 
            self.skipTest(f"Failed to connect to database. Error message: {err}")

        except Exception as err:
            logging.error(f"An error occurred while connecting to the database. {err}")
            self.skipTest(f"Failed to connect to database. Error message: {err}")

    def tearDown(self):
        # close cursor and connection
        self.cursor.close()
        self.connection.close()

    # def test_account_name(self):
    #     for i in range(len(self.rows)):
    #         self.assertEqual(self.rows[i][1], self.input_data[i]['accountName'])

    def test_account_name(self):
        try:
            account_names = [row[1] for row in self.rows]
            input_account_names = [data['accountName'] for data in self.input_data]
            # db_account_names = sorted(account_names)
            # json_account_names = sorted(input_account_names)
            db_account_names_set = set(account_names)
            json_account_names_set = set(input_account_names)
            logging.info("Checking Account Names Existence in Table")
            logging.warning("Account Names in Database Table Must match with Account Names in JSON Input Data File") 
            self.assertSetEqual(db_account_names_set, json_account_names_set)
        except AssertionError as e:
            logging.error(f"Assertion error: {e}")
            raise e 

    
    # def test_password(self):
    #     for i in range(len(self.rows)):
    #         self.assertEqual(self.rows[i][2], self.input_data[i]['password'])

    def test_password(self):
        try:
            logging.info("Checking Password matching of Password record in Database Table and Input Data File")
            mismatched_accounts = []
            for row in self.rows:
                account_name = row[1]
                db_password = row[2]
                for data in self.input_data:
                    if data['accountName'] == account_name:
                        input_password = data['password']
                        if db_password != input_password:
                            mismatched_accounts.append(account_name)
                        break
            self.assertListEqual(mismatched_accounts, [], f"Passwords mismatch for accounts: {mismatched_accounts}")
        except AssertionError as e:
            logging.error(f"Assertion error: {e}")
            raise e 


    def test_number_of_records(self): 
        try:
            logging.info("test_number_of_records to check for number of records present in Msys Accounts table with Input Data Records.")
            logging.warning("To pass test_number_of_records Test Method Both Number of Records should be same..") 
            self.assertEqual(len(self.rows), len(self.input_data), "Number of records are not equal") 
        except AssertionError as e:
            logging.error(f"Assertion error: {e}")
            raise e 

    def test_account_id(self):
        try:
            logging.info("test_account_id method tests that account Id generated is not Null")
            self.user_ID_list = [i[0] for i in self.rows]
            for element in self.user_ID_list:
                with self.subTest(element = element):
                    self.assertIsNotNone(element)
        except AssertionError as e:
            logging.error(f"Assertion error: {e}")
            raise e 
         

if __name__ == '__main__':
    unittest.main()
