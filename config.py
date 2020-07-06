import os
import sqlite3
import pymysql
import app
from flask import Flask
class Config:
    SECRET_KEY = 'mrsoft'
    UP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app/static/uploads/")
    FC_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app/static/uploads/users/")
    @staticmethod
    def init_app(app):
        pass
class DevelopmentConfig(Config):
    app = Flask(__name__)
    base_dir = os.path.abspath(os.path.join(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@127.0.0.1:3306/lening_log'
    DEBUG = True

# define the config
config = {
    'default': DevelopmentConfig
}