from flask import Flask, jsonify, request, Response, json

# from instance.config import app_config
from instance.config import app_config

def create_app(config_name):

  from app.models import find_question,valid_answer,update_question
  app = Flask(__name__,instance_relative_config=True)

  #Add an answer
  @app.route('/stack_overflow/api/v1/questions/<int:questionId>/answers', methods=['POST']) 
  def add_answer(questionId):
    request_data  = request.get_json()
    question = find_question(questionId)

    if valid_answer(request_data) and question:
      answerId = len(question['answers']) + 1
      
      answer = {
          'answerId': answerId,
          'questionId': questionId,
          'answer': request_data['answer'],

      }
      question['answers'].append(answer)

      update_question(questionId, question)
      return Response(json.dumps(answer), 201, mimetype="application/json") 

    else:
      bad_object = {
          "error": "Invalid answer object",
          "help_string":
              "Request format should be {'answer': 'the server is down'}"
      }
      return Response(json.dumps(bad_object), status=400, mimetype="application/json")
      
  return app
