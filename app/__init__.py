from flask import Flask, jsonify, request, Response, json
from app.models import questions


def create_app():
    app = Flask(__name__)

    # Fetch all questions
    @app.route('/stack_overflow/api/v1/questions', methods=['GET'])
    def get_questions():
        return jsonify({'questions': questions})

    # Fetch a specific question
    @app.route('/stack_overflow/api/v1/questions/<int:questionId>', methods=['GET'])
    def get_a_question(questionId):
        for question in questions:
            if question.get('questionId') == questionId:
                return jsonify({"question": question})
        return jsonify({"error": "Question Not Found"}), 404

    #adding a question
    @app.route('/stack_overflow/api/v1/questions', methods=['POST'])
    def add_question():
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "application expects json object"}), 400

				 
        question_id = questions[-1].get('questionId') + 1
        question = {
            'questionId': question_id,
            'question': request_data.get('question'),
            'description': request_data.get('description'),						
            'answers': []
        }
        questions.append(question)
        return Response(json.dumps(question), 201, mimetype="application/json")

    # Add an answer
    @app.route('/stack_overflow/api/v1/questions/<int:questionId>/answers', methods=['POST'])
    def add_answer(questionId):
      request_data = request.get_json()

      if not request_data:
          return jsonify({"error": "application expects json object"}), 400

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

    return app
