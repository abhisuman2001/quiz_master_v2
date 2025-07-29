import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # This hardcoded key removes all environment-related errors
    SECRET_KEY = 'a-super-secret-and-static-key-that-will-not-change'
    JWT_SECRET_KEY = 'a-super-secret-and-static-key-that-will-not-change'

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///quiz_master.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')