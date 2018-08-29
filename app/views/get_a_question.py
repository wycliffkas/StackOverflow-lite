from flask import Flask, jsonify, request, Response, json
from app.models import questions
from app import app

# Fetch a specific question
@app.route('/stack_overflow/api/v1/questions/<int:questionId>', methods=['GET'])
def get_a_question(questionId):
    for question in questions:
        if question.get('questionId') == questionId:
            return jsonify({"question": question})
    return jsonify({"error": "Question Not Found"}), 404