from .import SQLAlchemy,create_app
from datetime import datetime
db = SQLAlchemy(create_app())
class Topic(db.Model):
    __tablename__ = "topic"
    id = db.Column(db.Integer, primary_key=True)
    topic_s = db.Column(db.String(100)) 
    enty_id = db.Column(db.Integer,db.ForeignKey('empty.id')) 
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    def __str__(self):
        return '<topic %r>' % self.topic_s
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    def __repr__(self):
        return '<User %r>' % self.name
class Empty(db.Model):
    __tablename__ = "empty"
    id = db.Column(db.Integer, primary_key=True)
    empty = db.Column(db.String(1000))
    add_time =  db.Column(db.DateTime,index=True,default=datetime.now)
    topic_id = db.Column(db.Integer,db.ForeignKey('topic.id'))
    def __repr__(self):
        return '<Empty %r>' % self.empty
