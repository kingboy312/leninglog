from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_object(config['default'])
    db.init_app(app)
    config['default'].init_app(app)
    app.config["DEBUG"] = True
    from app.home import home as home_blueprint
    from app.admin import admin
    app.register_blueprint(home_blueprint)
    app.register_blueprint(admin,url_prefix="/admin")
    return app

