import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'movies.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
