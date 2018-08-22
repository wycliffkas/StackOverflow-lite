import module_import
from app.application import App
import unittest

class test_authentication(unittest.TestCase):
    ## Login set up now.
    def setUp(self):
        self.app_login = App()

    ## Test if user input is empty 
    def test_empty_fields(self):
        ##app_login = App()
        result = self.app_login.login('', '')
        ##self.assertEqual(True, result, 'Username and password cannot be empty')
        self.assertFalse(result, "Username and Password cannot be empty")

    ## Test if the matches for username and password work
    def test_login_match(self):
        result = self.app_login.login('chadwalt', 'chadwalt2')
        self.assertTrue(result, "Passwords didn't match")

    ## Test to check if the account already exists.
    def test_already_exists_account(self):        
        result = self.app_login.signup('timothy', 'kyadondo', 'chadwalt', 'chadwalt2', '')
        self.assertTrue(result, "User already exists")

    ## Test for the return type is a list of users.
    def test_list_users(self):
        result = self.app_login.list_users()
        self.assertEqual(type(result), 'list', 'This has to be a list of users')

    ## Test for empty fields for the signup
    def test_empty_fields_signup(self):
        result = self.app_login.signup('', '', '', '', '')
        self.assertFalse(result, 'Fields cannot be empty')        

if __name__ == '__main__':
    unittest.main()