import unittest
from flask import Flask,jsonify, json
from app import app
from flask_jwt_extended import JWTManager,jwt_required,create_access_token,get_jwt_identity
from app.models import DatabaseModel
jwt = JWTManager(app)
db_connect = DatabaseModel('postgresql://testuser:password123@localhost:5432/testdb')

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.access_token = create_access_token(identity="okello")
        self.headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
        self.answer = {'answer': 'restart the computer'}
        self.question = {'question': 'mukwano gwa makerere', 'description': 'i always get a 404 Error when i visit my website'}
        self.upvote = {'vote': 'yes'}
        self.downvote = {'vote': 'no'}
        db_connect.create_tables()



    def test_adding_an_answer(self):
        response = app.test_client().post('/stack_overflow/api/v1/questions',data = json.dumps(self.question),
            content_type = 'application/json',headers=self.headers)
        self.assertEqual(response.status_code,201) 

        response = app.test_client().post('/stack_overflow/api/v1/questions/1/answers',
        data = json.dumps(self.answer),content_type = 'application/json',headers=self.headers)
        self.assertEqual(response.status_code,201) 

    def test_answering_question_that_doesnt_exist(self):
        response = app.test_client().post('/stack_overflow/api/v1/questions/1000/answers',
        data = json.dumps(self.answer),content_type = 'application/json',headers=self.headers)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,404) 
        self.assertEqual(str(response_data["message"]),"No question with the specified Question Id in the database")


    def test_updating_an_answer_with_wrong_id(self):
        response = app.test_client().post('/stack_overflow/api/v1/questions',data = json.dumps(self.question),
            content_type = 'application/json',headers=self.headers)
        self.assertEqual(response.status_code,201) 

        response = app.test_client().put('/stack_overflow/api/v1/questions/1/answers/1000',
        data = json.dumps(self.answer),content_type = 'application/json',headers=self.headers)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,404) 
        self.assertEqual(str(response_data["message"]),"Wrong Id, please check the question or Answer ID")


    def test_upvoting_answer(self):
        response = app.test_client().post('/stack_overflow/api/v1/questions',data = json.dumps(self.question),
        content_type = 'application/json',headers=self.headers)
        self.assertEqual(response.status_code,201) 

        response = app.test_client().post('/stack_overflow/api/v1/questions/1/answers',
        data = json.dumps(self.answer),content_type = 'application/json',headers=self.headers)
        self.assertEqual(response.status_code,201) 

        response = app.test_client().post('/stack_overflow/api/v1/answers/vote/1',
        data = json.dumps(self.upvote),content_type = 'application/json',headers=self.headers)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,201) 
        self.assertEqual(str(response_data["message"]),"Answer successfully up voted")        


    def test_downvoting_answer(self):
        response = app.test_client().post('/stack_overflow/api/v1/questions',data = json.dumps(self.question),
        content_type = 'application/json',headers=self.headers)
        self.assertEqual(response.status_code,201) 

        response = app.test_client().post('/stack_overflow/api/v1/questions/1/answers',
        data = json.dumps(self.answer),content_type = 'application/json',headers=self.headers)
        self.assertEqual(response.status_code,201) 
                
        response = app.test_client().post('/stack_overflow/api/v1/answers/vote/1',
        data = json.dumps(self.downvote), content_type = 'application/json',headers=self.headers)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,201) 
        self.assertEqual(str(response_data["message"]),"Answer successfully down voted")     
             

    def tearDown(self):
        db_connect.tear_down()

if __name__ == '__main__':
    unittest.main() 