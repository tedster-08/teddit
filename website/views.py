from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db

views = Blueprint('views', __name__)


@views.route("/")
@login_required
def home():
    posts = Post.query.order_by(Post.date).all()
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

    return render_template("new_post.html", page_title="New Post", user=current_user)
