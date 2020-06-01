from flask import render_template, request, redirect, url_for
import bcrypt
from application import app, db
from application.auth.models import User, Role
from application.auth.forms import LoginForm, RegisterForm
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
    return redirect(url_for("index"))


@app.route("/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form=RegisterForm())

    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("auth/registerform.html", form=form, action="Register")

    u = User(
        username=form.username.data,
        full_name=form.full_name.data,
        password=form.password.data,
        email=form.email.data,
    )

    db.session.add(u)
    db.session().commit()
    login_user(u, remember=True)
    return redirect(url_for("index"))
