from flask import Flask

app = Flask(__name__)
    # app.config.from_object(DevelopmentConfig)
    # app.config['JWT_SECRET_KEY'] = 'SECRET' 
    # JWTManager(app)
from app import views




