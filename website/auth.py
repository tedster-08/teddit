from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password!", category="error")
        else:
            flash("There is no user with that name!", category="error")
    return render_template("login.html", page_title="Login", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        password_conf = request.form.get("password-conf")

        user = User.query.filter_by(username=username).first()

        if user:
            flash("A user already exists with that username!", category="error")
        elif email == "":
            flash("Enter an email!", category="error")
        elif username == "":
            flash("Enter a username!", category="error")
        elif password == "":
            flash("Enter a password!", category="error")
        elif password != password_conf:
            flash("Passwords don't match!", category="error")
        elif len(password) < 3:
            flash("Password must be at least 3 characters", category="error")
        else:
            new_user = User(email=email, username=username,
                            password=generate_password_hash(
                                password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")

            return redirect(url_for('views.home'))

    return render_template("signup.html", page_title="Sign Up", user=current_user)
