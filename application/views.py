from flask import render_template
from application import app, db
from sqlalchemy import text
from flask_login import current_user
from application.auth.models import User
from application.events.models import Event


@app.route("/")
def index():
    myevents = None
    if current_user.is_authenticated:
        myevents = User.query.get(current_user.id).events
        myevents = [e.id for e in myevents]
    popular_events = Event.event_summary().fetchall()
    print(len(popular_events))
    return render_template("index.html", events=popular_events, myevents=myevents)
