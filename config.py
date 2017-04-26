"""
config.py

Configuration and settings
"""
import os


class Config(object):
    DEBUG = False
    TESTING = False
    USERNAME = "admin"
    PASSWORD = "secret"
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI",
                                        'postgresql+psycopg2://postgres:postgres@localhost:5433/nest_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class Production(Config):
    DEBUG = False
    TESTING = False

    
class Development(Config):
    DEBUG = True
    TESTING = False


class Testing(Config):
    DEBUG = False
    TESTING = True
