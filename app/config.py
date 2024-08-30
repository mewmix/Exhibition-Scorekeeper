import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'MOOOCOWMOOOOOO')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///scorekeeper.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
