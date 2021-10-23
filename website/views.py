from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route("/")
@login_required
def home():
    return render_template("index.html", user=current_user)


@views.route("/post", methods=["GET", "POST"])
def new_post():
    return render_template("new_post.html", page_title="New Post", user=current_user)
