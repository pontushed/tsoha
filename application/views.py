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
        WITH t4 AS (
            SELECT t1.*, count(t2.user_id) participants FROM event t1
            INNER JOIN events_participants t2
            ON t2.event_id=t1.id
            GROUP BY t1.id
        )
        SELECT t3.name venue_name, t3.location venue_location, t4.*, account.full_name as organizer
        FROM venue t3 LEFT JOIN t4 ON t4.venue_id = t3.id
        INNER JOIN account ON t4.admin_id=account.id
        WHERE t4.end_time > date('now')
    """
    )
    return db.engine.execute(stmt)
