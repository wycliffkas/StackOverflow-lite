import pytest
from app import create_app
import json
import os

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

def test_get_questions():
  """Test API can fetch all questions"""
  response = app.test_client().get('/stack_overflow/api/v1/questions')
  assert response.status_code == 200


















