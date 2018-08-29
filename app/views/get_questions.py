from flask import Flask, jsonify, request, Response, json
from app.models import questions
from app import app

@app.route('/stack_overflow/api/v1/questions', methods=['GET'])
def get_questions():
    return jsonify({'questions': questions})