from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required
)
from werkzeug.security import generate_password_hash, check_password_hash

from modelui import db, User

auth = Blueprint("auth", __name__)

login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        username = email  # email doubles as the username

        if not email or not password:
            flash("All fields are required.")
            return redirect(url_for("auth.signup"))

        existing_email = User.query.filter_by(email=email).first()

        if existing_email:
            flash("An account with that email already exists.")
            return redirect(url_for("auth.signup"))

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully! Please log in.")
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        login_input = request.form.get("login", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter(
            (User.username == login_input) |
            (User.email == login_input)
        ).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.")

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))