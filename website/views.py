
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort
from flask_login import login_required, current_user
from .models import Post, User
from . import db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER, allowed_file
import json
from werkzeug.utils import secure_filename
import datetime

views = Blueprint('views', __name__)


@views.route("/")
@login_required
def home():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template("index.html", user=current_user, posts=posts, user_cls=User)


@views.route("/post/", methods=["GET", "POST"])
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


@views.route('/profiles/<username>/')
def user_page(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template("user_page.html", page_title=f"Profile: {user.username}", current_user=current_user, user=user, user_cls=User)


@views.route("/change-email", methods=["GET", "POST"])
def change_email():
    return render_template("change_email.html", page_title="Change Email", user=current_user)


@views.route("/change-password", methods=["GET", "POST"])
def change_password():
    return render_template("change_password.html", page_title="Change Password", user=current_user)


@views.route("/change-profile-picture", methods=["GET", "POST"])
def change_profile_picture():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part', category="error")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', category="error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename_format = f"pfp_user_{current_user.id}"
            filename_format = f"user_{current_user.id}_" + \
                str(datetime.datetime.utcnow().timestamp())
            _, ext = os.path.splitext(file.filename)
            filename = secure_filename(
                filename_format) + ext
            full_filename = os.path.join(os.path.dirname(
                __file__), UPLOAD_FOLDER, filename)
            file.save(full_filename)
            old_filename = os.path.join(os.path.dirname(
                __file__), UPLOAD_FOLDER, current_user.pfp_filename)
            if old_filename and os.path.exists(old_filename):
                os.remove(old_filename)
            current_user.pfp_filename = filename
            db.session.commit()
            return redirect(url_for(f'views.user_page', username=current_user.username))
    return render_template("change_pfp.html", page_title="Change Profile Picture", user=current_user)
