from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm): 
    title = StringField('제목', validators=[DataRequired()])
    text = TextAreaField('내용', validators=[DataRequired()])
    submit = SubmitField('작성하기')