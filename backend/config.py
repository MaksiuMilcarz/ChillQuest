import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    # Use absolute path with 4 slashes for SQLite in Docker
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////app/instance/travel_tracker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration - simpler configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # 24 hours
    
    # Basic JWT settings
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    
    # Debug settings to make Flask-JWT more forgiving
    JWT_IDENTITY_CLAIM = "sub"  # Must match what's in the token
    JWT_ERROR_MESSAGE_KEY = "message"
    
    # CORS Settings
    CORS_HEADERS = 'Content-Type,Authorization,X-Requested-With'