import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Changed to SQLite! This will automatically create a file called smart_attendance.db
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'sqlite:///smart_attendance.db' 
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-final-year-key-9988')
    SECRET_KEY = os.getenv('SECRET_KEY', 'flask-session-secret-key')