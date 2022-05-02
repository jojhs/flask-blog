from crypt import methods
from turtle import title
from flask import render_template, url_for, flash, request, redirect, abort, Blueprint
from flask_login import current_user, login_required
from blog import db
from blog.models import Post
from blog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

# CREATE 
@posts.route('/create', methods=['GET','POST'])
@login_required
def create(): 
    form = PostForm()
    
    if form.validate_on_submit() :     
        post = Post(title=form.title.data, 
                        text=form.text.data,
                        user_id=current_user.id) 
        db.session.add(post)
        db.session.commit()
        flash('블로그 포스트가 생성 되었습니다.')
        return redirect(url_for('core.index'))
    
    return render_template('create_post.html', form=form)
    
# BLOG POST (VIEW)
# post_id 정수형으로 캐스팅
@posts.route('/<int:post_id>')
def post(post_id): 
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, date=post.date, post=post)

# UPDATE 
@posts.route('/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update(post_id): 
    post = Post.query.get_or_404(post_id)
    
    # 포스트를 작성한 사용자가 아니면 403 에러 전달
    if post.author != current_user: 
        # abort : Flask가 제공하는 함수 -> 오류코드 전달
        abort(403)
    
    # 포스트를 작성한 사용자면, 폼 생성 후 변경사항 커밋
    form = PostForm()
    if form.validate_on_submit() :     
        post.title = form.title.data
        post.text = form.text.data
        
        db.session.commit()
        flash('블로그 포스트 수정이 완료 되었습니다.')
        
        # 수정 완료본을 확인 할 수 있도록 해당 포스트로 리다이렉트
        return redirect(url_for('posts.post', post_id=post_id))
    
    elif request.method == 'GET' : 
        form.title.data = post.title
        form.text.data = post.text
    
    return render_template('create_post.html', title='포스트 수정', form=form)

# DELETE 
@posts.route('/<int:post_id>/delete', methods=['GET','POST'])
@login_required
def delete(post_id): 
    post = Post.query.get_or_404(post_id)
    
    # 포스트를 작성한 사용자가 아니면 403 에러 전달
    if post.author != current_user: 
        # abort : Flask가 제공하는 함수 -> 오류코드 전달
        abort(403)
    
    # 포스트를 작성한 사용자면, 해당 포스트 삭제 후 커밋
    db.session.delete(post)
    db.session.commit()
    flash('블로그 포스트 삭제가 완료 되었습니다.')
    
    return redirect(url_for('core.index'))