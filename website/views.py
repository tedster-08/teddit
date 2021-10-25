from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User
from . import db
import json

views = Blueprint('views', __name__)


@views.route("/")
@login_required
def home():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template("index.html", user=current_user, posts=posts, user_cls=User)


@views.route("/post", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        post_title = request.form.get("post-title")
        post_text = request.form.get("post-text")

        if not post_title:
            flash("You must add a post title!", category="error")
        elif not post_text:
            flash("You cannot create an empty post.", category="error")
        else:
            new_post = Post(
                title=post_title, text=post_text, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash("Post created.", category="success")
            return redirect(url_for('views.home'))

    return render_template("new_post.html", page_title="New Post", user=current_user,)


@views.route('/delete-post',  methods=["POST"])
def delete_post():
    data = json.loads(request.data)
    post_id = data['id']
    post = Post.query.get(post_id)
    if post:
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()
            return jsonify({})
