import pytest
from app.models import *

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

def test_valid_question_object():
  questions = {'question': 'how to use an if statement','description': 'how can i use if statement in python'}
  result =  valid_question(questions)
  assert result == True

def test_invalid_question_object():
  questions = {'description': 'how can i use if statement in python'}
  result =  valid_question(questions)
  assert result == False





