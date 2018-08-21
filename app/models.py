
#checks if a question follows right format
def valid_question(questionObject):
  if "question" in questionObject and "description" in questionObject:
      return True
  return False

#checks if the answer follows right answer format
def valid_answer(answerObject):
  if "answer" in answerObject:
      return True
  return False

#returns a question with specified id
def find_question(id): 
  for question in questions:
    if question['questionId'] == id:
      return  question
  return "question is not in the database"

#adds an answer onto the question object
def update_question(id,updated_question): 
  for question in questions:
    if question['questionId'] == id:
      question.update(updated_question)
      return True
  return False


questions = [
  {
    'questionId': 1,
    'question': 'how to use an if statement',
    'description': 'how can i use if statement in python',
    'answers': [
        {
          'answerId': 1,
          'questionId': 1,
          'answer': 'begin with an if keyword',
        },
        {
          'answerId': 2,
          'questionId': 1,
          'answer': 'if: statement else: statement',
        }
    ]
  }
]