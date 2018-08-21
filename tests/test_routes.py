import pytest
from app import create_app
import json

app = create_app()


def test_get_questions():
  """Test API can fetch all questions"""
  response = app.test_client().get('/stack_overflow/api/v1/questions')
  assert response.status_code == 200


def test_get_a_question():
  """Test API can fetch a specific question"""
  response = app.test_client().get('/stack_overflow/api/v1/questions/1')  
  assert response.status_code == 200


def test_add_question():
  """Test API can add a question"""
  response = app.test_client().post(
    '/stack_overflow/api/v1/questions',
    data = json.dumps({'question': 'how to use an if statement','description': 'how can i use if statement in python'}),
    content_type = 'application/json'
    )
  response_data = json.loads(response.get_data(as_text=True))  

  assert response.status_code == 201
  assert response_data['questionId'] == 3
  assert response_data['question'] == "how to use an if statement"
  assert response_data['description'] == "how can i use if statement in python"
  assert response_data['answers'] == []


def test_add_answer():
  """Test API can add an answer"""  
  response = app.test_client().post(
    '/stack_overflow/api/v1/questions/1/answers',
    data = json.dumps({'answer': 'begin with an if keyword'}),
    content_type = 'application/json'
  )
  response_data = json.loads(response.get_data(as_text=True))
  assert response.status_code == 201
  assert response_data['answer'] == "begin with an if keyword"
  assert response_data['answerId'] == 3
  assert response_data['questionId'] == 1


















