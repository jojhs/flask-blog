from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from blog import db
from blog.models import Post
from blog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

# CREATE 
@posts.route('/create', methods=['GET','POST'])
@login_required
def create_post(): 
    form = PostForm()
    
    if form.validate_on_submit() :     
        post = PostForm(title=form.title.data, 
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
# DELETE 