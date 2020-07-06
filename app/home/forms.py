from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField,FieldList
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError
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
        render_kw={
            "class":"form-control ckedior"
        })  
    submit = SubmitField(
        'add',
        render_kw={
            "class": "btn btn-primary",
        }
    )
class registerforme(FlaskForm):
    username = StringField(
        validators=[
            DataRequired("用户名不能为空！"),
        ],
        description="用户名",
        render_kw={
            "placeholder": "请输入用户名！",
        }
    )
    email = StringField(
        validators=[
            DataRequired("邮箱不能为空！"),
            Email("邮箱格式不正确！")
        ],
        description="邮箱",
        render_kw={
            "type": "email",
            "placeholder": "请输入邮箱！",
        }
    )
    pwd = PasswordField(
        validators=[
            DataRequired("密码不能为空！")
        ],
        description="密码",
        render_kw={
            "placeholder": "请输入密码！",
        }
    )
    repwd = PasswordField(
        validators=[
            DataRequired("请输入确认密码！"),
            EqualTo('pwd', message="两次密码不一致！")
        ],
        description="确认密码",
        render_kw={
            "placeholder": "请输入确认密码！",
        }
    )
    submit = SubmitField(
        '注册',
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
            raise ValidationError("邮箱已经存在！")