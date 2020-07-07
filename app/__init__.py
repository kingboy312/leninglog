from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config,DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['default'])
    
    config['default'].init_app(app)
    app.config["DEBUG"] = True
    from app.home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    return app
app = create_app()
db = SQLAlchemy(app)