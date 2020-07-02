from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config,DevelopmentConfig

def create_app():
    app_ = DevelopmentConfig()
    app = app_.app
    app.config = config
    from app.home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    return app
app = create_app()
db = SQLAlchemy(app)