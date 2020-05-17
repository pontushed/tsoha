from flask import render_template, request, redirect, url_for
import bcrypt
from application import app
from application.auth.models import User
from application.auth.forms import LoginForm
from flask_login import login_user, logout_user


@app.route("/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()
    if not user:
        return render_template(
            "auth/loginform.html", form=form, erroru="No such username"
        )
    if not user.is_correct_password(form.password.data):
        return render_template(
            "auth/loginform.html", form=form, errorp="Invalid password"
        )
    login_user(user)
    print("User " + user.username + " authenticated!")
    return redirect(url_for("index"))


@app.route("/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
