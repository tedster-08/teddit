from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", page_title="Login")


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    return "<h1>LOGOUT</h1>"


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        password_conf = request.form.get("password-conf")

        if password == "":
            flash("Enter a password!", category="error")
        elif password != password_conf:
            flash("Passwords don't match!", category="error")
        else:
            flash("Account created.", category="success")
    return render_template("signup.html", page_title="Sign Up")
