from flask import Flask, jsonify, request, Response, json
from app.models import questions
from app import app

# Add an answer
@app.route('/stack_overflow/api/v1/questions/<int:questionId>/answers', methods=['POST'])
def add_answer(questionId):
  request_data = request.get_json()

  for question in questions:
      if question.get('questionId') == questionId:
        if not question['answers']:
            answerId = 1
            answer = {
                    'answerId': answerId,
                    'questionId': questionId,
                    'answer': request_data.get('answer')
            }
            question['answers'].append(answer)
            return Response(json.dumps(answer), 201, mimetype="application/json")            
        else:
            answerId = question['answers'][-1].get('answerId') + 1
            answer = {
                    'answerId': answerId,
                    'questionId': questionId,
                    'answer': request_data.get('answer')
            }
            question['answers'].append(answer)
            return Response(json.dumps(answer), 201, mimetype="application/json")
  return jsonify({"error": "question doesn't exist"}), 404