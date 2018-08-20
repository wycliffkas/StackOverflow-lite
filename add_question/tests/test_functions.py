import pytest
from app.models import valid_question

def test_valid_question_object():
  questions = {'question': 'how to use an if statement','description': 'how can i use if statement in python'}
  result =  valid_question(questions)
  assert result == True

def test_invalid_question_object():
  questions = {'description': 'how can i use if statement in python'}
  result =  valid_question(questions)
  assert result == False


