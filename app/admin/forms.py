from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField,FieldList
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError, length, Length
from app.models import *
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
        description="密码",
        render_kw={
            "type"       : "password",
            "placeholder": "Please enter your password!",
            "class":"validate-password",
            "size": 38,
            "maxlength": 99
        }
    )
    submit = SubmitField(
        'login',
        render_kw={
            "class": "btn btn-primary login",
        }
    )
class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="The old password",
        validators=[
            DataRequired("Old password cannot be empty!")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "Please enter your old password!",
        }
    )
    new_pwd = PasswordField(
        label="The new password",
        validators=[
            DataRequired("New password cannot be empty!")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "Please enter a new password!",
        }
    )
    submit = SubmitField(
        'save',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = User.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误！")