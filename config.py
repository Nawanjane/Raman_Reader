import os

class Config:
    SECRET_KEY = os.urandom(24)  # Random secret key for CSRF protection and session management
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Database URI for SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking
    UPLOAD_FOLDER = 'uploads'  # Folder where files will be uploaded
