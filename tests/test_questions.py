import unittest
from flask import Flask,jsonify, json
from app import app
from flask_jwt_extended import JWTManager,jwt_required,create_access_token,get_jwt_identity
import os
# from app.models import DatabaseModel
# from app.models import DatabaseModel, TearDownDatabase
from app.models import DatabaseModel
from instance.config import app_config
jwt = JWTManager(app)
os.environ['APP_SETTING']  = 'testing'

# db_connect = app.config['DATABASE_URL']
db_connect = DatabaseModel('postgresql://testuser:password123@localhost:5432/testdb')

# db_connect = DatabaseModel(app.config['DATABASE_URL'])
# app.config.from_object(app_config['testing'])
# import pdb; pdb.set_trace()

class TestQuestions(unittest.TestCase):
    def setUp(self):
        # import pdb; pdb.set_trace()
        self.app_context = app.app_context()
        self.app_context.push()
        self.access_token = create_access_token(identity="okello")
        self.headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
        self.question = {'question': 'mukwano gwa makerere', 'description': 'i always get a 404 Error when i visit my website'}
        db_connect.create_tables()
        
    def test_adding_a_question(self):
        response = app.test_client().post('/stack_overflow/api/v1/questions',data = json.dumps(self.question),
            content_type = 'application/json',headers=self.headers)
        self.assertEqual(response.status_code,201)      

    def test_fetching_all_question(self):
        response = app.test_client().post('/stack_overflow/api/v1/questions',data = json.dumps(self.question),
            content_type = 'application/json',headers=self.headers)

        response = app.test_client().get('/stack_overflow/api/v1/questions',headers=self.headers)
        self.assertEqual(response.status_code,201)

    def test_fetching_a_question(self):
        response = app.test_client().post('/stack_overflow/api/v1/questions',data = json.dumps(self.question),
            content_type = 'application/json',headers=self.headers)
        response = app.test_client().get('/stack_overflow/api/v1/questions/1',headers=self.headers)
        self.assertEqual(response.status_code,201)

    def test_posting_missing_required_fields(self):
        response = app.test_client().post('/stack_overflow/api/v1/questions',
        data = "",content_type = 'application/json',headers=self.headers)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,400) 
        self.assertEqual(str(response_data["message"]),"Invalid values posted, please make sure you have added all the fields") 

    def test_deleting_a_question(self):
        response = app.test_client().post('/stack_overflow/api/v1/questions',data = json.dumps(self.question),
            content_type = 'application/json',headers=self.headers)
        response = app.test_client().delete('/stack_overflow/api/v1/questions/1',headers=self.headers)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,201)
        self.assertEqual(str(response_data["message"]),"question was succesfully deleted")

    # def test_fetching_all_questions_by_user(self):
    #     response = app.test_client().get('/stack_overflow/api/v1/questions/user',headers=self.headers)
    #     self.assertEqual(response.status_code,201)  

    # def tearDown(self):
    #     TearDownDatabase.tear_down('postgresql://testuser:password123@localhost:5432/testdb')

    def tearDown(self):
        db_connect.tear_down()
        

if __name__ =='__main__':
    unittest.main()

