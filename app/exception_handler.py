
from flask import Flask, jsonify
from app.models import questions
from app import app

@app.errorhandler(400)
def missing_values(e):
    return jsonify("Invalid values posted, please make sure you have added all the fields"), 400

@app.errorhandler(404)
def values_not_found(e):
    return jsonify("Invalid values posted, please make sure the Id specified already exists in the database"), 404








  