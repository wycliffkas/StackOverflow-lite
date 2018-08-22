import module_import
from app.model import Users
import unittest

class BaseTest(unittest.TestCase):
    ## Login set up now.
    def setUp(self):
        self.bucket = Users()

    ## Test empty fields.
    def test_adding_bucket_item(self):
        result = self.bucket.add_bucket('', '')
        ##self.assertEqual(True, result, 'Username and password cannot be empty')
        self.assertFalse(result['success'], "Bucket Name cannot be empty")

    ## Test empty fields.
    def test_edit_bucket_item(self):
        result = self.bucket.edit_bucket(1, '', '')
        self.assertFalse(result['success'], "ID and name cannot be empty")   

    ## Test for empty ids
    def test_delete_bucket(self):
        result = self.bucket.delete_bucket(0)
        self.assertFalse(result['success'], "ID cannot be empty")  

    
if __name__ == '__main__':
    unittest.main()