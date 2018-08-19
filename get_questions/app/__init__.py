from flask import Flask, jsonify, request, Response, json

# from instance.config import app_config
from instance.config import app_config

def create_app(config_name):

  from app.models import questions
  app = Flask(__name__, instance_relative_config=True)

  # Fetch all questions
  @app.route('/stack_overflow/api/v1/questions', methods=['GET'])
  def get_questions():
    results = []

    for question in questions:
      results.append(
      question['question']
      )

    return jsonify(results)
      
  return app
