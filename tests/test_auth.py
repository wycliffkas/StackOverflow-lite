import unittest, json
from app import create_app, db

class AuthTestCase(unittest.TestCase):
    """
    Test cases for the auth blueprint
    """
    def setUp(self):
        """ Set the test variables """
        self.app = create_app(configuration='testing')
        self.client = self.app.test_client()
        self.user_data = {
            'username': 'kaka',
            'email': 'kaka@email.com',
            'password': 'hard-to-guess-1090'
        }

        with self.app.app_context():
            # Drop all existing tables and re-create them
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_user_registration(self):
        """Test user can create a new account"""
        response = self.client.post('/auth/register', data= json.dumps(self.user_data), content_type='application/json')
        # Return the results in json format
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'] , "Hey kaka, you have been successfully registered")

    def test_already_registered_user(self):
        """Test user cannot be registered twice"""
        first_registration = self.client.post('/auth/register', data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(first_registration.status_code, 201)
        second_registration = self.client.post('/auth/register', data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(second_registration.status_code, 409)   # Data conflict
        result = json.loads(second_registration.data.decode())
        self.assertEqual(result['message'], "That email already exists, please use a different one")

    def test_login(self):
        """Test registered user can login"""
        registration = self.client.post("/auth/register", data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(registration.status_code, 201)

        login = self.client.post("/auth/login", data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(login.status_code, 200)

        result = json.loads(login.data.decode())
        self.assertEqual(result['message'], "You are successfully logged in")
        self.assertTrue(result['access_token'])

    def test_non_registered_user_login(self):
        """Test non registered users cannot login"""
        non_user = {
            "username": "nani",
            "email": "nani@nana.com",
            "password": "nana"
        }

        response = self.client.post('/auth/login', data=json.dumps(non_user), content_type='application/json')
        self.assertEqual(response.status_code, 401)

        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "You are not yet registered. Please sign up for an account first")

    def test_logout(self):
        """Test a logged in user can logout"""
        registration = self.client.post("/auth/register", data=json.dumps(self.user_data), content_type='application/json')
        login = self.client.post('/auth/login', data=json.dumps(self.user_data), content_type='application/json')

        response = json.loads(login.data.decode())
        response['access_token'] = None
        self.assertFalse(response['access_token'])

    def test_password_change(self):
        """Test user can change password"""
        registration = self.client.post("/auth/register", data=json.dumps(self.user_data), content_type='application/json')
        login = self.client.post('/auth/login', data=json.dumps(self.user_data), content_type='application/json')
        results = json.loads(login.data.decode())
        new_password = {
            "email": "kaka@email.com",
            "password": "very-very-hard, unusually-hard" 
        }
        reset_password = self.client.put('/auth/reset-password', data=json.dumps(new_password), content_type='application/json')

        new_results = json.loads(reset_password.data.decode())
        self.assertEqual(new_results['message'], "Your password has been successfully changed")
        