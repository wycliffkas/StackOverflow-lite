from flask import Flask, jsonify, request, Response, json

# from instance.config import app_config
from instance.config import app_config

def create_app(config_name):

  from app.models import valid_question,questions
  app = Flask(__name__, instance_relative_config=True)

  #Add a question
  @app.route('/stack_overflow/api/v1/questions', methods=['POST'])
  def add_question():
    request_data  = request.get_json()
    if (valid_question(request_data)):
      question_id = len(questions) + 1
      # import pdb; pdb.set_trace()
      question = {
          'questionId': question_id,
          'question': request_data['question'],
          'description': request_data['description'],
          'answers': []

      }
      questions.append(question)
      return Response(json.dumps(question), 201, mimetype="application/json")
        
    else:
      bad_object = {
          "error": "Invalid question object",
          "help_string":
              "Request format should be {'question': 'Error 500',"
              "'description': 'i keep getting 500 error when i reload my page'}"
      }
      return Response(json.dumps(bad_object), status=400, mimetype="application/json")  
      
  return app
