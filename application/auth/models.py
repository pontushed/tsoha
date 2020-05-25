from flask_security import RoleMixin, UserMixin
from application import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

# Define models
roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("account.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)

events_participants = db.Table(
    "events_participants",
    db.Column("user_id", db.Integer(), db.ForeignKey("account.id")),
    db.Column("event_id", db.Integer(), db.ForeignKey("event.id")),
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140), unique=True, nullable=False)
    full_name = db.Column(db.String(140))
    email = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.Binary(60), nullable=False)
    # password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )
    events = db.relationship("Event", backref="account", lazy=True)

    def __init__(self, **kwargs):
        self.username = kwargs["username"]
        self.email = kwargs["email"]
        self.password = kwargs["password"]
        if kwargs.get("full_name") == False:
            self.full_name = kwargs["username"]
        else:
            self.full_name = kwargs["full_name"]

    def __str__(self):
        return "User: " + self.username + "(" + self.full_name + "), " + self.email

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
