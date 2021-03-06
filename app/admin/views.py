import os
import uuid
from datetime import datetime
from app import db
from . import admin
from flask import render_template, redirect, url_for, flash, session, request, g, abort,make_response,current_app
from app.admin.forms import *
from app.models import User,Topic,Empty
from werkzeug.utils import secure_filename
from sqlalchemy import or_ , and_
from functools import wraps
def admin_login(f):
    """
    登录装饰器
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function
@admin.route("/")
@admin_login
def index():
    return render_template("admin/index.html")
@admin.route("/login/", methods=["GET", "POST"])
def login():
    """
    登录
    """
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["username"]).first()
        if not user and not User.query.filter_by(email=data["username"]).first() :
            flash("Email does not exist!", "err")
            return redirect(url_for("admin.login"))
        if not user.check_pwd(data["password"]) :
            flash("Password error!", "err")
            return redirect(url_for("admin.login"))
        if user.admin != 1:
            flash("Not the administrator","err")
            return redirect(url_for("admin.login"))

        session["admin_id"] = user.id
        session["admin"] = user.name
        return redirect(url_for("admin.index"))
    return render_template("admin/login.html", form=form)
@admin.route("/logout/")
@admin_login
def logout():
    session.pop("admin_id",None)
    session.pop("admin_name",None)
    return redirect(url_for("admin.login"))
@admin.route('/pwd/',methods=["GET","POST"])
@admin_login
def pwd():
    """
    后台密码修改
    """
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = User.query.filter_by(name=session["admin"]).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(admin)
        db.session.commit()
        flash("Password changed successfully, please log in again!", "ok")
        return redirect(url_for('admin.logout'))
    return render_template("admin/pwd.html", form=form)
@admin.route("/user/")
@admin_login
def user():
    users = User.query.all()
    return render_template("admin/users.html",user=users)