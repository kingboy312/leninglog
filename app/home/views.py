from . import *
from app.models import *
from app.home.forms import *
from flask import render_template, url_for, redirect, flash, session, request
from werkzeug.security import generate_password_hash
from sqlalchemy import and_
from functools import wraps
from app.home.forms import *
@home.route('/topic/')
def topic():
    topic = Topic.query.filter_by()
    return render_template("home/topics.html",topics = topic)
@home.route('/')
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
@home.route('/topic/<int:topicid>/')
def emty(topicid):
    enty = Empty.query.filter_by(topic_id= topicid)
    topic = Topic.query.filter_by(id = topicid).first()
    return render_template("home/topic.html", entries=enty,topic=topic)
@home.route("/new_enty/<int:topicid>/",methods=["GET", "POST"])
def new_enty(topicid):
    topic = Topic.query.filter_by(id=topicid).first()
    form = newentryforme()
    if form.validate_on_submit():  
        data = form.data 
        entry = Empty(
            empty=data["entry"],
            topic_id=str(topicid)
        )
        db.session.add(entry) 
        db.session.commit()
        return redirect(url_for("home.topic"),topicid)
    return render_template("home/new_entry.html",form=form,topic=topic)
@home.route("/users/register/", methods=["GET", "POST"])
def register():
    """
    注册功能
    """
    form = registerforme()
    if form.validate_on_submit():
        data = form.data 
        user = User(
            name = data["username"],
            email = data["email"],
            pwd = generate_password_hash(data["pwd"]),
        )
        db.session.add(user)
        db.session.commit()
        session["user_id"]=User.query.filter_by(email=data["email"]).first().id
        session["username"]=data["username"]
        return redirect(url_for("home.bat"))
    return render_template("home/register.html", form=form)
@home.route("/logout/")
def logout():
    session.pop("user_id",None)
    session.pop("username",None)
    return redirect(url_for("home.login"))
@home.route("/login/", methods=["GET", "POST"])
def login():
    """
    登录
    """
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(email=data["email"]).first()
        if not user :
            flash("邮箱不存在！", "err")
            return redirect(url_for("home.login"))
        if not user.check_pwd(data["pwd"]):
            flash("密码错误！", "err")
            return redirect(url_for("home.login"))

        session["user_id"] = user.id
        userlog = Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.index"))
    return render_template("home/login.html", form=form)