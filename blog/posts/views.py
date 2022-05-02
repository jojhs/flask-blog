from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from blog import db
from blog.models import Post
from blog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

