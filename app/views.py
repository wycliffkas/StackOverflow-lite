from flask import json,jsonify,request,Response
from app.models import Questions
from app import app

questions_obj = Questions()

@app.route('/', methods=['GET'])
def welcome():
    return jsonify('Welcome to the StackOverflow-lite')

#adding a question
@app.route('/stack_overflow/api/v1/questions', methods=['POST'])
def add_question():
    request_data = request.get_json()

    if request_data.get('question')  and request_data.get('description') and request_data.get('userId'):
        question = request_data.get('question') 
        description = request_data.get('description') 
        userId = request_data.get('userId')
        return Response(json.dumps(questions_obj.save_questions(question,description,userId)), 201, mimetype="application/json") 
    else:
        bad_object = {
                "error": "Invalid question",
                "help_string":
                    "question format should be {'question': 'how to start a computer',"
                    "'description': 'where do i click to start a computer','userId': 123 }"
            }
        return Response(json.dumps(bad_object), status=400, mimetype="appliation/json")

#fetch all questions
@app.route('/stack_overflow/api/v1/questions', methods=['GET'])
def get_questions():
    
    if len(questions_obj.fetch_all_questions()) > 0:
      return jsonify(questions_obj.fetch_all_questions()),200
    return Response(json.dumps("No questions added yet"), status=400, mimetype="appliation/json")
    

#fetch a question
@app.route('/stack_overflow/api/v1/questions/<int:questionId>', methods=['GET'])
def get_a_question(questionId):
    
    if questions_obj.fetch_a_question(questionId):
        return jsonify(questions_obj.fetch_a_question(questionId)),200 
    return jsonify("question with specified the Id doesnt exist"),404

# Add an answer
@app.route('/stack_overflow/api/v1/questions/<int:questionId>/answers', methods=['POST'])
def add_answer(questionId):
    request_data = request.get_json()
    
    if request_data.get('answer')  and request_data.get('userId'):
        questionId = questionId
        answer = request_data['answer']
        userId = request_data['userId']
        return jsonify(questions_obj.save_answer(questionId,answer,userId)),200 
    else:
        bad_object = {
                "error": "Invalid answer",
                "help_string":
                    "answer format should be {'answer': 'how to start a computer',"
                    "'userId': 123 }"
            }
        return Response(json.dumps(bad_object), status=400, mimetype="appliation/json")

#delete an answer
@app.route('/stack_overflow/api/v1/questions/<questionId>', methods=['POST'])
def delete_question(questionId):
    return jsonify(questions_obj.delete_question(questionId)),200 


  


