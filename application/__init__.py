import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_security import (
    RoleMixin,
    Security,
    SQLAlchemyUserDatastore,
    UserMixin,
    login_required,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# Create database connection object
db = SQLAlchemy(app)

# Use Bcrypt module
bcrypt = Bcrypt(app)

from application import views
from application.auth import models
from application.auth.models import Role, User
from application.auth import views
from application.comments import models
from application.events import models
from application.events import views
from application.venues import models
from application.venues import views

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


db.create_all()

# Create a user to test with
@app.before_first_request
def create_user():
    u = User(
        username="admin",
        full_name="Administrator",
        password="admin",
        email="admin@localhost",
    )
    if not user_datastore.get_user("admin@localhost"):
        db.session.add(u)
        db.session.commit()


if __name__ == "__main__":
    app.run()
