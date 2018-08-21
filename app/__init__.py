from flask import Flask,jsonify,request,Response,json
from app.models import *

def create_app():
  app = Flask(__name__)

  # Fetch all questions
  @app.route('/stack_overflow/api/v1/questions', methods=['GET','POST'])
  def get_questions():
    if request.method == 'GET':
      return jsonify({'questions': questions})
    


  #Fetch a specific question
  @app.route('/stack_overflow/api/v1/questions/<int:questionId>', methods=['GET','POST'])
  def get_a_question(questionId):
    if request.method == 'GET':
      for item in questions:
        if item['questionId'] == questionId:
          question ={
            'questionId': item['questionId'],
            'question': item['question']
          }
      return jsonify(question)
   

  #Add a question
  @app.route('/stack_overflow/api/v1/questions', methods=['POST'])
  def add_question():
    if request.method == 'POST': 
      request_data  = request.get_json()
      if (valid_question(request_data)):
        question_id = questions[-1]['questionId'] + 1
        question = {
            'questionId': question_id,
            'question': request_data['question'],
            'description': request_data['description'],
            'answers': []

        }
        questions.append(question)
        return Response(json.dumps(question), 201, mimetype="application/json")
      bad_object = {
          "error": "Invalid question object",
          "help_string":
              "Request format should be {'question': 'Error 500',"
              "'description': 'i keep getting 500 error when i reload my page'}"
      }
      return Response(json.dumps(bad_object), status=400, mimetype="application/json") 
        

  #Add an answer
  @app.route('/stack_overflow/api/v1/questions/<int:questionId>/answers', methods=['POST']) 
  def add_answer(questionId):
    if request.method == 'POST':
      request_data  = request.get_json()
      question = find_question(questionId)

      if valid_answer(request_data) and question:
        answerId = question['answers'][-1]['answerId'] + 1
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
