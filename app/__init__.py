from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config,DevelopmentConfig

def create_app():
    app_ = DevelopmentConfig()
    app = app_.app
    db = SQLAlchemy(app)
    db.init_app(app)
    db.create_all()
    from app.home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    return app
app = Flask(__name__)
db = SQLAlchemy(app)