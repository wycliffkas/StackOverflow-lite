import pytest
from app.models import find_question,valid_answer

def test_valid_answer_object():
  answer = {'answer': 'begin with an if keyword'}  
  result = valid_answer(answer)
  assert result == True

def test_invalid_answer_object():
  answer = {'question': 'begin with an if keyword'}  
  result = valid_answer(answer)
  assert result == False 

def test_invalid_question_id():
  result = find_question(100)
  assert result == "question is not in the database"


