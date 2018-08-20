import pytest
from app import create_app
import json
import os

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

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


















