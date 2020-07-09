from . import *
from app.models import *
from flask import render_template, url_for, redirect, flash, session, request
from werkzeug.security import generate_password_hash
from sqlalchemy import and_
from functools import wraps
from app.home.forms import *
def user_login(f):
    """
    登录装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["user_id"] == None:
            return redirect(url_for("home.login"))
        return f(*args, **kwargs)

    return decorated_function

@home.route('/topic/')
@user_login
def topic():
    topic = Topic.query.filter_by(user_id=session["user_id"]).all()
    return render_template("home/topics.html",topics = topic)
@home.route('/')
def bat():
    return render_template("home/bat.html")
@home.route("/new_topic/",methods=["GET", "POST"])
@user_login
def add_topic():
    form = new_topic_forme()           
    if form.validate_on_submit():  
        data = form.data 
        topic_s = Topic(
            topic_s= data["topic"],
            user_id= session["user_id"]
        )
        db.session.add(topic_s) 
        db.session.commit()
        return redirect("/topic/")
    return render_template("home/new_topic.html",form = form)
@home.route('/topic/<int:topicid>/')
@user_login
def emty(topicid):
    enty = Empty.query.filter_by(topic_id= topicid)
    topic = Topic.query.get_or_404(topicid)
    if topic.user_id != session["user_id"]:
        return redirect(url_for("home.no",id=topicid))
    return render_template("home/topic.html", entries=enty,topic=topic)
@home.route("/new_enty/<int:topicid>/",methods=["GET", "POST"])
@user_login
def new_enty(topicid):
    topic = Topic.query.filter_by(id=topicid).first()
    if topic.user_id != session["user_id"]:
        return redirect(url_for("home.no",id=topicid))
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
        session["user_id"]=User.query.filter_by(name=data["username"]).first().id
        session["username"]=data["username"]
        return redirect(url_for("home.bat"))
    return render_template("home/register.html", form=form)
@home.route("/logout/")
@user_login
def logout():
    session['user_id']=None
    session['username']=None
    return redirect(url_for("home.login"))
@home.route("/login/", methods=["GET", "POST"])
def login():
    """
    登录
    """
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["username"]).first()
        if not user :
            flash("邮箱不存在！", "err")
            return redirect(url_for("home.login"))
        if not user.check_pwd(data["password"]) :
            flash("密码错误！", "err")
            return redirect(url_for("home.login"))

        session["user_id"] = user.id
        session["username"] = user.name
        return redirect(url_for("home.bat"))
    return render_template("home/login.html", form=form)
@home.route("/topic/<int:id>/no/")
def no(id):
    return redirect(url_for("home.topic"))
@home.errorhandler(404)
def page_not_found(error):
    """
    404
    """
    return render_template("home/404.html"), 404