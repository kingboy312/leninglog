from .import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    admin = db.Column(db.Integer,default=0)
    def __repr__(self):
        return '<User %r>' % self.name
    def check_pwd(self,pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)
class Topic(db.Model):
    __tablename__ = "topic"
    id = db.Column(db.Integer, primary_key=True)
    topic_s = db.Column(db.String(100))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    def __str__(self):
        return '<topic %r>' % self.topic_s
class Empty(db.Model):
    __tablename__ = "empty"
    id = db.Column(db.Integer, primary_key=True)
    empty = db.Column(db.String(1000))
    add_time = db.Column(db.DateTime,index=True,default=datetime.now)
    topic_id = db.Column(db.Integer,db.ForeignKey('topic.id'))
    def __repr__(self):
        return '<Empty %r>' % self.empty
class o_s(db.Model):
    __tablename__ = "o_s"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    o_s = db.Column(db.String(1000))
    def __repr__(self):
        return '<o_s %r>' % self.o_s