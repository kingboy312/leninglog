from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField,FieldList
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError, length, Length
from app.models import *
class new_topic_forme(FlaskForm):
    topic = StringField(
        validators=[
            DataRequired("not noll！"),
        ],
        description="new_topic:",
        render_kw={
            "placeholder": "new_topic",
        })
    submit = SubmitField(
        'add',
        render_kw={
            "class": "btn btn-primary",
        }
    )
class newentryforme(FlaskForm):
    entry = TextAreaField(
        validators=[
            DataRequired("Item content cannot be empty!")
        ],
        description="The entry content",
        render_kw={
            "class":"form-control ckeditor",
            "rows": 10
        }

    )
    submit = SubmitField(
        'add',
        render_kw={
            "class": "btn btn-primary",
        }
    )
class registerforme(FlaskForm):
    username = StringField(
        label="username：",
        validators=[
            DataRequired("User name cannot be empty!"),
        ],
        description="用户名",
        render_kw={
            "placeholder": "Please enter user name!",
        }
    )
    email = StringField(
        label="email：",
        validators=[
            DataRequired("The mailbox cannot be empty!"),
            Email("Incorrect email format!")
        ],
        description="邮箱",
        render_kw={
            "type": "email",
            "placeholder": "Please enter email!",
        }
    )
    pwd = PasswordField(
        label="password：",
        validators=[
            DataRequired("Password cannot be empty!")
        ],
        description="密码",
        render_kw={
            "placeholder": "Please enter your password!",
        }
    )
    repwd = PasswordField(
        label="password(again)：",
        validators=[
            DataRequired("Please enter your confirmation password!"),
            EqualTo('pwd', message="The two passwords don't match!")
        ],
        description="确认密码",
        render_kw={
            "placeholder": "Please enter your confirmation password!",
        }
    )
    submit = SubmitField(
        'register',
        render_kw={
            "class": "btn btn-primary",
        }
    )
    def validate_email(self, field):
        """
        检测注册邮箱是否已经存在
        :param field: 字段名
        """
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError("Email already exists!")
class LoginForm(FlaskForm):
    username = StringField(
        validators=[
            DataRequired("User name cannot be empty!"),
            Length(min=3, max=50, message="The user name must be between 3 and 10 digits long")
        ],
        description="用户名",
        render_kw={
            "type"       : "text",
            "placeholder": "Please enter user name!",
            "class":"validate-username",
            "size" : 38,
            "maxlength" : 99
        }
    )
    password = PasswordField(
        validators=[
            DataRequired("Password cannot be empty!"),
            Length(min=3, message="Password length is not less than 6 digits")
        ],
        description="password",
        render_kw={
            "type"       : "password",
            "placeholder": "Please enter your password!",
            "class":"validate-password",
            "size": 38,
            "maxlength": 99
        }
    )
    submit = SubmitField(
        'The login',
        render_kw={
            "class": "btn btn-primary login",
        }
    )
class Opinion_suggestionform(FlaskForm):
    name = StringField(
        label="name",
        validators=[
            DataRequired("The name cannot be empty!")
        ],
        description="name",
        render_kw={
            "class": "form-control",
            "placeholder": "Please enter your name!",
        }
    )
    email = StringField(
        label="email",
        validators=[
            DataRequired("The email cannot be empty!")
        ],
        description="email",
        render_kw={
            "class": "form-control",
            "placeholder": "Please enter your email!",
        }
    )
    o_s = TextAreaField(
        label="Opinion suggestion",
        validators=[
            DataRequired("The Opinion suggestion cannot be empty!")
        ],
        description="Opinion suggestion",
        render_kw={
            "class": "form-control",
            "placeholder": "Please enter your Opinion suggestion!",
            "rows": 7
        }
    )
    submit = SubmitField(
        'ok',
        render_kw={
            "class": "btn btn-primary login",
        }
    )