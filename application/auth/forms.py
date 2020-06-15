from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    StringField,
    BooleanField,
    validators,
    ValidationError,
)
from application.auth.models import User


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False


class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=4, max=40)])
    password = PasswordField("Password", [validators.Length(min=8, max=40)])
    full_name = StringField(
        "Full name",
        [
            validators.InputRequired("Please enter your full name."),
            validators.Length(max=60),
        ],
    )
    email = StringField(
        "Email",
        [
            validators.InputRequired("Please enter your email address."),
            validators.Email("This field requires a valid email address"),
            validators.length(max=255),
        ],
    )

    class Meta:
        csrf = False

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose another one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose another one.")


class ProfileForm(RegisterForm):
    password = PasswordField(
        "Reset Password", [validators.Optional(), validators.Length(min=8, max=40)]
    )
    isadmin = BooleanField("User is an admin")

    def validate_username(self, username):
        return

    def validate_email(self, email):
        return
