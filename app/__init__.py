from flask import Flask,jsonify,request,Response,json
from app.models import *

def create_app():
  app = Flask(__name__)

  # Fetch all questions
  @app.route('/stack_overflow/api/v1/questions', methods=['GET'])
  def get_questions():
    return jsonify({'questions': questions})  


  #Fetch a specific question
  def get_a_question(questionId):
    pass
   

  #Add a question
  def add_question():
    pass
        

  #Add an answer
  def add_answer(questionId):
    pass


  return app
