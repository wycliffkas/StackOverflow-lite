import pytest
from app import app
import json
from app.models import Questions
from datetime import date

questions_obj = Questions()
date_added = date.today().strftime("%d/%m/%Y")

def test_getting_questions_from_an_empty_database():
  """Test fetching questions from an empty dataset"""
  response = app.test_client().get('/stack_overflow/api/v1/questions')
  assert response.status_code == 400
  response_message = json.loads(response.data.decode())
  assert response_message == "No questions added yet"

def test_getting_questions_already_in_the_dataset():
  """Test fetching questions after adding them"""
  response = app.test_client().post('/stack_overflow/api/v1/questions',
    data = json.dumps({
      'questionId': 1,
      'question': "i get a 404 error",
      'description': "i always get a 404 error when i call localhost",
      'userId': 1,
      'answers':[],
      'date_added': date_added
      }),
    content_type = 'application/json')
  response_data = json.loads(response.get_data(as_text=True)) 
  assert response.status_code == 201
  assert response_data['questionId'] == 1
  assert response_data['question'] == "i get a 404 error"
  assert response_data['description'] == "i always get a 404 error when i call localhost"
  assert response_data['answers'] == []
  assert response_data['date_added'] == date_added

def test_getting_a_question_that_doesnt_exist_in_dataset():
  """Test fetching a question with an id that doesnt exist in the dataset"""
  response = app.test_client().get('/stack_overflow/api/v1/questions/300')
  assert response.status_code == 404
  response_message = json.loads(response.data.decode())
  assert response_message == "question with specified the Id doesnt exist"

def test_getting_a_question_already_in_dataset():
  """Test fetching a question with an id that exists in the dataset"""
  response = app.test_client().post('/stack_overflow/api/v1/questions/1',
    data = json.dumps({
      'questionId': 1,
      'question': "i get a 404 error",
      'description': "i always get a 404 error when i call localhost",
      'userId': 1,
      'answers':[],
      'date_added': date_added
      }),
    content_type = 'application/json')
  response_data = json.loads(response.get_data(as_text=True)) 
  assert response.status_code == 200
  assert response_data['questionId'] == 1
  assert response_data['question'] == "i get a 404 error"
  assert response_data['description'] == "i always get a 404 error when i call localhost"
  assert response_data['answers'] == []
  assert response_data['date_added'] == date_added

def test_posting_empty_answer_object():
  """Test empty json object as answer"""  
  response = app.test_client().post(
    '/stack_overflow/api/v1/questions/1/answers',
    data = json.dumps({ }),
    content_type = 'application/json'
  )
  assert response.status_code == 400

def test_posting_empty_question_object():
  """Test API can add a question"""
  response = app.test_client().post(
    '/stack_overflow/api/v1/questions',
    data = json.dumps({}),
    content_type = 'application/json'
    )
  assert response.status_code == 400
 
def test_add_answer():
  """Test API can add an answer"""  
  response = app.test_client().post(
    '/stack_overflow/api/v1/questions/1/answers',
    data = json.dumps({'answer': 'begin with an if keyword'}),
    content_type = 'application/json'
  )
  assert response.status_code == 201
  







