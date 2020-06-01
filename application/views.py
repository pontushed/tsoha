from flask import render_template
from application import app, db
from sqlalchemy import text
from flask_login import current_user
from application.auth.models import User


@app.route("/")
def index():
    myevents = None
    if current_user.is_authenticated:
        myevents = User.query.get(current_user.id).events
        myevents = [e.id for e in myevents]
    popular_events = event_summary()
    return render_template("index.html", events=popular_events, myevents=myevents)


def event_summary():
    stmt = text(
        """
        SELECT t2.name as venue_name, t2.location as venue_location, t1.*,
        COUNT(t3.user_id) as participants, account.full_name as organizer
        FROM Event t1
        LEFT JOIN Venue t2 on t1.venue_id=t2.id
        INNER JOIN events_participants t3 ON t3.event_id=t1.id
        INNER JOIN account ON t1.admin_id=account.id
        WHERE t1.end_time > date('now')
        GROUP BY t2.name"""
    )
    return db.engine.execute(stmt)
