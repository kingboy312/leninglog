from . import *
from app.models import User,Topic,Empty,o_s
from flask import render_template, url_for, redirect, flash, session, request,current_app,make_response
from werkzeug.security import generate_password_hash
from sqlalchemy import and_
from functools import wraps
from app.home.forms import *
import os
import uuid
from werkzeug.utils import secure_filename
def user_login(f):
    """
    登录装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "user_id" in session:
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
        user = User.query.filter_by(name=data["username"]).first()
        if not user and not User.query.filter_by(email=data["username"]).first() :
            flash("Email or user name does not exist!", "err")
            return redirect(url_for("home.login"))
        if not user.check_pwd(data["password"]) :
            flash("Password error!", "err")
            return redirect(url_for("home.login"))

        session["user_id"] = user.id
        session["username"] = user.name
        return redirect(url_for("home.bat"))
    return render_template("home/login.html", form=form)
@home.route("/topic/<int:id>/no/")
def no(id):
    return render_template("home/404.html")
@home.errorhandler(404)
def page_not_found(error):
    """
    404
    """
    return render_template("home/404.html"), 404
@home.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor 文件上传"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")

    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)

        filepath = os.path.join(current_app.static_folder, 'uploads/ckeditor', rnd_name)
        print(filepath)
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'

        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('uploads/ckeditor', rnd_name))
    else:
        error = 'post error'

    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)

    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response
def gen_rnd_filename():
    return datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex)
@home.route("/edit_entry/<int:entry_id>/",methods=["GET", "POST"])
def edt_entry(entry_id):
    entry = Empty.query.get_or_404(entry_id)
    topic = Topic.query.get_or_404(entry.topic_id)
    form = newentryforme()
    if form.validate_on_submit():
        data = form.data
        Empty.query.filter_by(id=entry_id).update({"empty":data["entry"]})
        db.session.commit()
        return redirect(url_for("home.topic"))
    elif request.method == "GET":
        form.entry.data = entry.empty
        form.submit.label.text = "edt"
    return render_template("home/edt_entry.html",form=form,entry=entry,topic=topic)
# @home.route("/Opinion_suggestion/",methods=["GET", "POST"])
# @user_login
# def Opinion_suggestion():
#     form = Opinion_suggestionform()
#     if form.validate_on_submit():
#
#         data = form.data
#         o_s=o_s(
#             name=data["name"],
#             email=data["email"],
#             o_s=data["o_s"]
#         )
#         db.session.add(o_s)
#         db.session.commit()
#         return redirect(url_for("home.index"))
#     return render_template("home/user.html",form=form)