from crypt import methods
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import db 
from blog.models import User, Post
from blog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from blog.users.picture_handler import add_profile_picture

users = Blueprint('users', __name__)

#register
@users.route('/register', methods=['GET', 'POST'])
def register(): 
    form = RegistrationForm() 
    
    #submit 버튼이 눌렀을때 유효한 경우 
    if form.validate_on_submit() : 
        user = User(email=form.email.data, 
                    username=form.username.data, 
                    password=form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash('회원 가입을 해주셔서 감사드립니다. 로그인 페이지로 이동 시켜 드릴테니 로그인 해주세요.')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form)
            
#login
@users.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm() 
    if form.validate_on_submit() : 
        # 로그인 하려는 사용자의 이메일이 DB에 유니크하게 등록되어 있는지 확인
        user = User.query.filter_by(email=form.email.data).first()
        
        # DB에 등록되어 있다면, 비밀번호 맞는지 체크 후 로그인
        if user.check_password(form.password.data) and user is not None: 
            login_user(user) 
            flash('로그인에 성공 하였습니다.')
            print('로그인에 성공 하였습니다.')
            # 사용자가 접근하려 했던 경로 확인 후 리다이렉트
            next = request.args.get('next')
            if next == None or not next[0] == '/' : 
                next = url_for('core.index')
                
            return redirect(next)
        
    return render_template('login.html', form=form)

#logout
@users.route('/logout')
def logout(): 
    logout_user()
    return redirect(url_for('core.index'))

#account (update UserForm) 
@users.route('/accout', methods=['GET', 'POST'])
@login_required
def account(): 
    form = UpdateUserForm()
    if form.validate_on_submit(): 
        if form.picture.data: 
            username = current_user.username
            picture = add_profile_picture(form.picture.data, username)
            current_user.profile_image = picture
        
        current_user.username = form.username.data
        current_user.email = form.username.data
        
        db.session.commit()
        flash('계정 정보가 수정 되었습니다.')
        return redirect(url_for('users.account'))
    
    # 사용자가 아무것도 제출하지 않는 경우 현재 사용자 이름과 이메일 가져옴
    elif request.method == 'GET' : 
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    # 계정 페이지의 템플릿 렌더링
    profile_image = url_for('static', filename='images/profile'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

# 특정 사용자에 대한 블로그 포스팅 가져오기
@users.route('/<username>')
def user_posts(username): 
    page = request.args.get('pages', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', posts=posts, user=user)
