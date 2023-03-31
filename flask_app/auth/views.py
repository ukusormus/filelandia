from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import logout_user, current_user, login_user

from flask_app.auth.forms import LoginForm, RegisterForm
from flask_app.extensions import db, login_manager
from flask_app.models import User

auth = Blueprint("auth", __name__, static_folder="../static", url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        # Checks passed (POST request; username and password are correct)

        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)

        flash("Login successful")
        return redirect(url_for("index"))

    return render_template("auth/login.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/")

    form = RegisterForm()
    if form.validate_on_submit():
        # Checks passed (POST request; username and password validators in forms.py)
        # Create new user and add them to the database
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash("Account created!")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)
