from flask import Flask
from flask_cors import CORS
# import connexion

# # Create the application instance
# app = connexion.App(__name__, specification_dir='./')

# #read te swagger.yml file to configure the endpoints
# app.add_api('swagger.yml')

app = Flask(__name__)


CORS(app)
from app import views




