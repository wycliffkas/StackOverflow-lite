import unittest
from flask import Flask,jsonify, json
from app import app
from flask_jwt_extended import JWTManager,jwt_required,create_access_token,get_jwt_identity
from app.models import DatabaseModel
from instance.config import app_config
jwt = JWTManager(app)
db_connect = DatabaseModel('postgresql://testuser:password123@localhost:5432/testdb')

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.user_signup = {'fullname':'wycokas','username':'wyco','email':'wyco@gmail.com','password': 'wyco123'} 
        self.user_signin = {'username':'wyco','password': 'wyco123'}  
        self.wrong_username_signin = {'username':'chad','password': 'wyco123'} 
        self.wrong_password_signin = {'username':'wyco','password': 'chad1234'} 
        db_connect.create_tables()

    def test_user_signup(self):
        response = app.test_client().post('/stack_overflow/api/v1/auth/signup',
        data = json.dumps(self.user_signup),content_type = 'application/json')
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,201)
        self.assertEqual(str(response_data["message"]),"user registered successfully")

    def test_user_signup_with_already_used_username(self):
        response = app.test_client().post('/stack_overflow/api/v1/auth/signup',
        data = json.dumps(self.user_signup),content_type = 'application/json')
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,201)
        self.assertEqual(str(response_data["message"]),"user registered successfully")
        
        response = app.test_client().post('/stack_overflow/api/v1/auth/signup',
        data = json.dumps(self.user_signup),content_type = 'application/json')
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,400)
        self.assertEqual(str(response_data["message"]),"pick another username, user already exits")          


    def test_user_login(self):
        response = app.test_client().post('/stack_overflow/api/v1/auth/signup',
        data = json.dumps(self.user_signup),content_type = 'application/json')
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,201)
        self.assertEqual(str(response_data["message"]),"user registered successfully")

        response = app.test_client().post('/stack_overflow/api/v1/auth/login',
        data = json.dumps(self.user_signin),content_type = 'application/json')
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(str(response_data["message"]),"user successfully logged in")  

    def test_login_with_wrong_username(self):
        response = app.test_client().post('/stack_overflow/api/v1/auth/signup',
        data = json.dumps(self.user_signup),content_type = 'application/json')
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,201)
        self.assertEqual(str(response_data["message"]),"user registered successfully")

        response = app.test_client().post('/stack_overflow/api/v1/auth/login',
        data = json.dumps(self.wrong_username_signin),
            content_type = 'application/json')
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,400)
        self.assertEqual(str(response_data["message"]),"user with the above username doesnt exist in the database")    


    def test_login_with_wrong_password(self):
        response = app.test_client().post('/stack_overflow/api/v1/auth/signup',
        data = json.dumps(self.user_signup),content_type = 'application/json')
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,201)
        self.assertEqual(str(response_data["message"]),"user registered successfully")

        response = app.test_client().post('/stack_overflow/api/v1/auth/login',
        data = json.dumps(self.wrong_password_signin),
            content_type = 'application/json')
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,400)
        self.assertEqual(str(response_data["message"]),"Login failed,check your password")       
          

    def tearDown(self):
        db_connect.tear_down()

if __name__ == '__main__':
    unittest.main()

