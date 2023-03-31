from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp, EqualTo, ValidationError

from . import min_username_length, max_username_length, min_password_length, max_password_length, max_filename_length
from flask_app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        InputRequired(message="Please fill out your username."),
    ])

    password = PasswordField("Password", validators=[
        InputRequired(message="Please fill out your password.")
    ])

    submit = SubmitField("Log In")

    def validate(self, extra_validators=None):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user is None or not user.check_password(self.password.data):
            self.form_errors.append("Invalid username or password.")
            return False

        return True


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
        InputRequired(message="Username must not be empty."),
        Length(min=min_username_length, message="Username must be at least %(min)d characters."),
        Length(max=max_username_length, message="Username can't be longer than %(max)d characters."),
        Regexp(regex="^[A-Za-z0-9_.-]*$",
               message="Username can only contain letters, numbers, and symbols \".\" and \"-\".")
    ])

    password = PasswordField("Password", validators=[
        InputRequired(message="Password must not be empty."),
        Length(min=min_password_length, message="Password must be at least %(min)d characters."),
        Length(max=max_password_length, message="Password can't be longer than %(max)d characters."),
    ])
    password2 = PasswordField("Repeat Password", validators=[
        InputRequired(message="Repeat Password must not be empty."),
        EqualTo(fieldname="password", message="Repeat Password must match Password.")
    ])

    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is already taken, please use a different username.")
