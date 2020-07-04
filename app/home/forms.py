from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
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
    entry = StringField(
        validators=[
            DataRequired("not noll！"),
        ]
        description="new_entry:",
        render_kw={
            "placeholder": "new_topic",
            "size":38,
        })  
    submit = SubmitField(
        'add',
        render_kw={
            "class": "btn btn-primary",
        }
    )