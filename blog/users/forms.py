# 폼 설정을 위한 import
from flask import Flask
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# 사용자 설정을 위한 import
from flask_login import current_user
from blog.models import User

# 로그인 폼
class LoginForm(FlaskForm) : 
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    submit = SubmitField('로그인')

# 회원가입 폼
class RegistrationForm(FlaskForm) : 
    email = StringField('이메일', validators=[DataRequired(), Email()])
    username = StringField('사용자명', validators=[DataRequired()])
    password = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password_confirm', message='비밀번호가 일치하지 않습니다.')])
    password_confirm = PasswordField('비밀번호 확인', validators=[DataRequired()])
    submit = SubmitField('회원가입')
    
    def check_email(self, field): 
        if User.query.filter_by(email=field.data).first() : 
            raise ValidationError('이미 사용중인 이메일 입니다.')
    
    def check_username(self, field): 
        if User.query.filter_by(username=field.data).first() : 
            raise ValidationError('이미 사용중인 사용자명 입니다.')
        
# 회원정보관리 폼 
class UpdateUserForm(FlaskForm) : 
    email = StringField('이메일', validators=[DataRequired(), Email()])
    username = StringField('사용자명', validators=[DataRequired()])
    # FileAllowed() 안에 리스트로 업로드 할 수 있는 파일 확장자 제한
    # 여기서는 .jpg 와 .png 만 업로드 할 수 있음
    picture = FileField('프로필 이미지 수정', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('수정')
    
    def check_email(self, field): 
        if User.query.filter_by(email=field.data).first() : 
            raise ValidationError('이미 사용중인 이메일 입니다.')
    
    def check_username(self, field): 
        if User.query.filter_by(username=field.data).first() : 
            raise ValidationError('이미 사용중인 사용자명 입니다.')