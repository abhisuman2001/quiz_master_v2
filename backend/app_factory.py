from flask import Flask
from config import Config
from models import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from tasks import celery
from notifications import mail


from scheduler import init_scheduler


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    JWTManager(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    
    # Configure celery
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)
    
    # Initialize Flask-Mail
    mail.init_app(app)
    

    # Initialize scheduler
    init_scheduler(app)

    
    return app
    return app