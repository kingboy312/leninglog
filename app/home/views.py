from . import *
from app.models import *
from app.home.forms import *
from flask import render_template, url_for, redirect, flash, session, request
from werkzeug.security import generate_password_hash
from sqlalchemy import and_
from functools import wraps
from app.home.forms import *
@home.route('/')
def index():
    return render_template("home/index.html")
@home.route('/topic/')
def topic():
    topic = Topic.query.filter_by()
    return render_template("home/topics.html",topics = topic,Enty = Empty,topicid = None)
@home.route('/leninglog/')
def bat():
    return render_template("home/bat.html")
@home.route("/new_topic/",methods=["GET", "POST"])
def add_topic():
    form = new_topic_forme()           
    if form.validate_on_submit():  
        data = form.data 
        topic_s = Topic(
            topic_s= data["topic"]
        )
        db.session.add(topic_s) 
        db.session.commit()
        return redirect("/topic/")
    return render_template("home/new_topic.html",form = form)