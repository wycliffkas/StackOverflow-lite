from flask import json,jsonify,request,Response
from .models import Questions,Users,Answers
from flask_jwt_extended import JWTManager,jwt_required,create_access_token,get_jwt_identity
import datetime
from app import app

app.config['JWT_SECRET_KEY'] = 'stackoverflowbootcamp'  
jwt = JWTManager(app)

questions_obj = Questions()
users_obj = Users()
answers_obj = Answers()

#registering new users
@app.route('/stack_overflow/api/v1/auth/signup', methods=['POST'])
def signup():
    request_data = request.get_json()
    if request_data.get('fullname')  and request_data.get('username') and request_data.get('email') and request_data.get('password'):
        fullname = request_data.get('fullname') 
        username = request_data.get('username') 
        email = request_data.get('email')
        password = request_data.get('password')
        results = users_obj.save_users(fullname,username,email,password)
        return jsonify(results),201
    else:
        bad_object = {
                "error!": "all fields are required",
                "help_string":
                    "should have fields like {'fullname': 'wycliff','username':'wyco','email':wyco@gmail.com"
                    ",'password': 'wyco123'}"
        }
        return Response(json.dumps(bad_object), status=400, mimetype="appliation/json")
#login users
@app.route('/stack_overflow/api/v1/auth/login', methods=['POST'])
def login():
    request_data = request.get_json()
    username = request_data.get('username') 
    password = request_data.get('password')
    return users_obj.login_user(username, password)


#adding a question
@app.route('/stack_overflow/api/v1/questions', methods=['POST'])
@jwt_required
def add_question():
    request_data = request.get_json()
    
    if request_data.get('question')  and request_data.get('description'):
        question = request_data.get('question') 
        description = request_data.get('description') 
        results = questions_obj.save_questions(question,description)
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
    
    if len(questions_obj.fetch_all_questions()) > 0:
      return jsonify(questions_obj.fetch_all_questions()),200
    return jsonify({"Message":"No questions added yet"}),404
    

#fetch a question
@app.route('/stack_overflow/api/v1/questions/<int:questionId>', methods=['GET'])
@jwt_required
def get_a_question(questionId):
    
    results = questions_obj.fetch_a_question(questionId)
    return jsonify(results),404

#delete a question
@app.route('/stack_overflow/api/v1/questions/<questionId>', methods=['DELETE'])
@jwt_required
def delete_question(questionId): 
    return jsonify(questions_obj.delete_question(questionId)),200 

# Add an answer
@app.route('/stack_overflow/api/v1/questions/<questionId>/answers', methods=['POST'])
@jwt_required
def add_answer(questionId):
    request_data = request.get_json()
    if request_data:
        answer = request_data.get('answer')
        return jsonify(answers_obj.save_answer(questionId,answer)),200    
    else:
        bad_object = {
                "error": "Invalid answer",
                "help_string":
                    "answer format should be {'answer': 'how to start a computer'}"
            }
        return Response(json.dumps(bad_object), status=400, mimetype="appliation/json")


# update answer or accept an answer
@app.route('/stack_overflow/api/v1/questions/<questionId>/answers/<answerId>', methods=['PUT'])
@jwt_required
def update_answer(questionId,answerId):
    request_data = request.get_json()
    answer = request_data['answer']
    results = answers_obj.update_answer(questionId,answer,answerId)
    return jsonify(results),200




# upvote and downvote answer
@app.route('/stack_overflow/api/v1/answers/vote/<answerId>', methods=['POST'])
@jwt_required
def vote_answer(answerId):
    request_data = request.get_json()

    if request_data:
        vote = request_data['vote']
        message = answers_obj.vote_answer(answerId,vote)
        return jsonify(message),200    
    else:
        bad_object = {
                "error": "Invalid vote",
                "help_string":
                    "vote format should be {'vote': 'yes'}"
            }
        return Response(json.dumps(bad_object), status=400, mimetype="appliation/json")  


# all questions asked by the user
@app.route('/stack_overflow/api/v1/questions/user', methods=['GET'])
@jwt_required
def questions_asked_user():
        results = questions_obj.questions_asked_user()
        return jsonify(results),200        




@app.errorhandler(400)
def missing_values(e):
    return jsonify("Invalid values posted, please make sure you have added all the fields"), 400

@app.errorhandler(404)
def values_not_found(e):
    return jsonify("Invalid values posted, please make sure the Id specified already exists in the database"), 404






  


