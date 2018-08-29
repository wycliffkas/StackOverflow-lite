from flask import Flask, jsonify, request, Response, json
from app.models import questions
from app import app

#adding a question
@app.route('/stack_overflow/api/v1/questions', methods=['POST'])
def add_question():
  request_data = request.get_json()
  question_id = questions[-1].get('questionId') + 1
  question = {
      'questionId': question_id,
      'question': request_data['question'],
      'description': request_data['description'],						
      'answers': []
  }
  questions.append(question)
  return Response(json.dumps(question), 201, mimetype="application/json")