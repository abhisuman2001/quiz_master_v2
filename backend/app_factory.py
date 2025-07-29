from flask import Flask
from config import Config
from models import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from tasks import celery

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    JWTManager(app)
    
    # Configure celery
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)
    
    return app