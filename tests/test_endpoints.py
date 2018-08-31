import pytest
from app.models import Users, Questions, Answers
from app.views import app
from flask import jsonify, json
from flask_jwt_extended import JWTManager,jwt_required,create_access_token,get_jwt_identity

app.config['JWT_SECRET_KEY'] = 'stackoverflowbootcamp'  
jwt = JWTManager(app)

questions = Questions()
answers = Answers()
users = Users()



def test_already_registered_user():
    user = users.add_user_account( 'wyco', 'wyco', 'wyco@gmail.com', 'wyco')
    assert user == {"Message":"pick another username, user already exits"}

def test_for_user_account_creation():
    response = app.test_client().post('/stack_overflow/api/v1/auth/signup', data=json.dumps(users.add_user_account( 'wyco', 'wyco', 'wyco@gmail.com', 'wyco')), content_type="application/json")
    assert response.status_code == 201 

def test_if_question_is_added():
    assert isinstance(questions.save_questions('Error 500', 'what does error 500 mean'),  dict)

# def test_getting_a_question_already_in_dataset():
#     """Test fetching a question with an id that exists in the dataset"""
#     response = app.test_client().post('/stack_overflow/api/v1/questions/',
#         data = json.dumps({
#         'question': "i get a 404 error",
#         'description': "i always get a 404 error when i call localhost",
#         }),
#         content_type = 'application/json')
#     response_data = json.loads(response.get_data(as_text=True)) 
#     assert response_data['question'] == "i get a 404 error"
#     assert response_data['description'] == "i always get a 404 error when i call localhost"

# def test_if_user_is_able_to_login(self):
#     res = self.client().post('/signup', data=json.dumps(('mako', 'password')), content_type="application/json")
#     self.assertEqual(res.status_code, 200)

# def test_if_user_with_invalid_username_can_login(self):
#     res = self.client().post('/signup', data=json.dumps(('makchsj', 'password')), content_type="application/json")
#     self.assertEqual(res.status_code, 400)

# def test_if_user_with_invalid_password_can_login(self):
#     res = self.client().post('/signup', data=json.dumps(('mako', 'passwordaer')), content_type="application/json")
#     self.assertEqual(res.status_code, 400)

# def test_for_adding_questions(self):
#     res = self.client().post('/questions', data=json.dumps(self.quest.add_questions('musa', 'what icvbfs a boolean', "I got it from a forum")), content_type="application/json")
#     self.assertEqual(res.status_code, 201)

# def test_for_adding_a_blank_question(self):
#     res = self.client().post('/questions', data=json.dumps(self.quest.add_questions('', '', "")), content_type="application/json")
#     self.assertEqual(res.status_code, 400)

# def test_for_adding_already_existing_question(self):
#     res = self.client().post('/questions', data=json.dumps(self.quest.add_questions('musa', 'what icvbfs a boolean', "I got it from a forum")), content_type="application/json")
#     self.assertEqual(res.status_code, 400)

# def test_for_adding_a_null_question(self):
#     res = self.client().post('/questions', data=json.dumps(None), content_type="application/json")
#     self.assertEqual(res.status_code, 400)

# def test_for_viewing_all_questions(self):
#     res = self.client().get('/questions')
#     self.assertEqual(res.status_code, 200)

# def test_for_viewing_questions_when_database_is_empty(self):
#     res = self.client().get('/questions')
#     self.assertEqual(res.status_code, 404)

# def test_if_qid_out_of_range(self):
#     res = self.client().get('/questions/1000')
#     self.assertEqual(res.status_code, 400)

# def test_for_viewing_a_question(self):
#     res = self.client().get('/questions/1')
#     self.assertEqual(res.status_code, 200)

# def test_for_deleting_a_question(self):
#     res = self.client().delete('/questions/22')
#     self.assertEqual(res.status_code, 202)

# def test_for_selecting_preferred_answer(self):
#     res = self.client().put('/questions/1/answers/1')
#     self.assertEqual(res.status_code, 201)

# def test_for_adding_answers(self):
#     res = self.client().post('/questions/1/answers', data=json.dumps(self.ans.add_answer(1, 'collo', 'explangrgsgzgation of a bolean', 'This is a True/False scenario')), content_type="application/json")
#     self.assertEqual(res.status_code, 201)
