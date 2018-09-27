from flask import Flask,make_response,json,jsonify,request,Response,render_template
from app import app
from .models import DatabaseModel
from flask_jwt_extended import (
    JWTManager,jwt_required, create_access_token, get_jwt_identity)
import datetime
import os


# database_url = os.environ.get('DATABASE_URI')

# app = Flask(__name__)
# ctx = app.app_context()
# ctx.push()

# with ctx:
#     pass

from instance.config import app_config

# app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY') 
app.config['JWT_SECRET_KEY'] = "stackoverflowlite"
jwt = JWTManager(app)

app.config['SECRET_KEY'] = 'my-stackoverflow-key'

# app.config.from_object(app_config[os.environ.get('APP_SETTING')])

# app.config.from_object(app_config['testing'])
# database_url = os.environ.get('DATABASE_URL')
# db_connect = DatabaseModel(database_url)

db_connect = DatabaseModel('postgres://dofplzajzoyfvj:b6c3c11b2bff17446997688d0c003e87e6b49b2b569ce5d4b533ca03da4f4b4d@ec2-54-225-97-112.compute-1.amazonaws.com:5432/d6vclujglsl826')

#registering new users
@app.route('/stack_overflow/api/v1/auth/signup', methods=['POST'])
def signup():
    request_data = request.get_json()
    if request_data.get('fullname')  and request_data.get('username') and request_data.get('email') and request_data.get('password'):
        if len(request_data.get('password')) > 6:
            fullname = request_data.get('fullname') 
            username = request_data.get('username') 
            email = request_data.get('email')
            password = request_data.get('password')
            response = db_connect.save_users_database(fullname,username,email,password)
            return response
        else:
            response = {
                'message': 'Passwords should have more than 6 characters'
            }
            return jsonify(response)
    else:
        bad_object = {
                "error!": "all fields are required",
                "help_string":
                    "should have fields like {'fullname': 'wycliff','username':'wyco','email':wyco@gmail.com"
                    ",'password': 'wyco123'}"
        }
        return Response(json.dumps(bad_object), status=400, mimetype="application/json")

    
#login users
@app.route('/stack_overflow/api/v1/auth/login', methods=['POST'])
def login():
    request_data = request.get_json()
    username = request_data.get('username') 
    password = request_data.get('password')
    results = db_connect.verify_login(username, password)
    return results

   
#adding a question
@app.route('/stack_overflow/api/v1/questions', methods=['POST'])
@jwt_required
def add_question():
    request_data = request.get_json()
    if request_data.get('question')  and request_data.get('description'):
        question = request_data.get('question') 
        description = request_data.get('description') 
        results = db_connect.insert_questions_database(question,description)
        return jsonify(results),201
    else:
        bad_object = {
                "error": "Invalid question",
                "help_string":
                    "question format should be {'question': 'how to start a computer',"
                    "'description': 'where do i click to start a computer'}"
            }
        return Response(json.dumps(bad_object), status=400, mimetype="appliation/json")



#fetch all questions
@app.route('/stack_overflow/api/v1/questions', methods=['GET'])
@jwt_required
def get_questions():
    return db_connect.fetch_questions_database()
    
#fetch a question
@app.route('/stack_overflow/api/v1/questions/<int:questionId>', methods=['GET','POST'])
@jwt_required
def get_a_question(questionId):
    results = db_connect.fetch_a_question_database(questionId)
    return results
    
#delete a question
@app.route('/stack_overflow/api/v1/questions/<questionId>', methods=['DELETE'])
@jwt_required
def delete_question(questionId): 
    return db_connect.delete_question(questionId) 

# all questions asked by the user
@app.route('/stack_overflow/api/v1/questions/user', methods=['GET'])
@jwt_required
def questions_asked_user():
        results = db_connect.questions_asked_user_database()
        return results   

# Add an answer
@app.route('/stack_overflow/api/v1/questions/<questionId>/answers', methods=['POST'])
@jwt_required
def add_answer(questionId):
    request_data = request.get_json()
    if request_data:
        answer = request_data.get('answer')
        results = db_connect.save_answer(questionId,answer)
        return results
    else:
        bad_object = {
                "error": "Invalid answer",
                "help_string":
                    "answer format should be {'answer': 'restart the computer'}"
            }
        return Response(json.dumps(bad_object), status=400, mimetype="appliation/json")

# update answer or accept an answer
@app.route('/stack_overflow/api/v1/questions/<questionId>/answers/<answerId>', methods=['PUT'])
@jwt_required
def update_answer(questionId,answerId):
    request_data = request.get_json()
    answer = request_data['answer']
    results = db_connect.update_answer_database(questionId,answer,answerId)
    return results

# upvote and downvote answer
@app.route('/stack_overflow/api/v1/answers/vote/<answerId>', methods=['POST'])
@jwt_required
def vote_answer(answerId):
    request_data = request.get_json()

    if request_data:
        vote = request_data['vote']
        results = db_connect.vote_answer(answerId,vote)
        return results   
    else:
        bad_object = {
                "error": "Invalid vote",
                "help_string":
                    "vote format should be {'vote': 'yes'}"
            }
        return Response(json.dumps(bad_object), status=400, mimetype="appliation/json")      

@app.errorhandler(400)
def missing_values(e):
    return jsonify({'message':'Invalid values posted, please make sure you have added all the fields'}), 400

# @app.errorhandler(404)
# def values_not_found(e):
#     return jsonify({'message':'Invalid values posted, please make sure the Id specified already exists in the database'}), 404





  


