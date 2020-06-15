from flask import render_template, request, redirect, url_for
import bcrypt
from application import app, db, login_required
from application.auth.models import User, Role
from application.auth.forms import LoginForm, RegisterForm, ProfileForm
from application.events.models import Event
from flask_login import login_user, logout_user, current_user


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


@app.route("/profile", methods=["GET", "POST"])
@login_required
def auth_profile():
    u = User.query.get(current_user.id)
    events_organized = Event.query.filter_by(admin_id=current_user.id)
    if request.method == "GET":
        return render_template(
            "auth/profile.html", data=u, events_organized=events_organized
        )


@app.route("/users", methods=["GET"])
@login_required(role="admin")
def users_list():
    users = User.query.all()
    return render_template("auth/list.html", users=users)


@app.route("/users/delete/<user_id>", methods=["POST"])
@login_required(role="admin")
def users_delete(user_id):
    u = User.query.get(user_id)
    db.session.delete(u)
    db.session().commit()
    return redirect(url_for("users_list"))


@app.route("/users/edit/<user_id>", methods=["GET"])
@login_required(role="admin")
def users_edit(user_id):
    u = User.query.get(user_id)
    form = ProfileForm(obj=u)
    form.isadmin.data = "admin" in u.get_roles()
    events_organized = Event.query.filter_by(admin_id=current_user.id)
    return render_template(
        "auth/edit_user.html", form=form, data=u, events_organized=events_organized
    )


@app.route("/users/edit/<user_id>", methods=["POST"])
@login_required(role="admin")
def users_update(user_id):
    form = ProfileForm(request.form)
    u = User.query.get(user_id)
    events_organized = Event.query.filter_by(admin_id=current_user.id)
    if not form.validate():
        return render_template(
            "auth/edit_user.html", form=form, data=u, events_organized=events_organized
        )

    u.username = form.username.data
    u.full_name = form.full_name.data
    u.email = form.email.data
    if len(form.password.data) > 7 and len(form.password.data) < 41:
        u.password = form.password.data
    if form.isadmin.data:
        u.roles = [Role.query.get(1)]
    else:
        u.roles = []
    db.session().commit()

    return redirect(url_for("users_list"))
