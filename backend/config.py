import os

#TODO Replace with database url shit
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:Atomic1@localhost/music_processor")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "uploads/"
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")