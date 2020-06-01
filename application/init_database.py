from application import app, db, user_datastore
from application.auth.models import User
from application.events.models import Event
from application.venues.models import Venue
from datetime import datetime, timedelta
from flask import url_for, redirect

# Test credentials should not be in the code. This will be removed later.
# Create a user and a couple of venues and events to test with.
@app.route("/init")
def create_user():
    Venue.query.delete()
    Event.query.delete()
    User.query.delete()
    db.session.commit()
    u = User(
        username="admin",
        full_name="Administrator",
        password="admin",
        email="admin@localhost",
    )
    db.session.add(u)
    v = Venue(name="Gurula", location="Exactum")
    db.session.add(v)
    v = Venue(name="Klusteri", location="Leppäsuonkatu 12, Helsinki")
    db.session.add(v)

    e = Event(
        admin_id=1,
        name="Testitapahtuma",
        info="Testi",
        venue_id=1,
        start_time=datetime.now() + timedelta(hours=2),
        end_time=datetime.now() + timedelta(hours=4),
    )
    db.session().add(e)
    e = Event(
        admin_id=1,
        name="Testitapahtuma2",
        info="Testi2",
        venue_id=2,
        start_time=datetime.now() + timedelta(hours=2),
        end_time=datetime.now() + timedelta(hours=4),
    )
    db.session().add(e)
    db.session.commit()

    return redirect(url_for("index"))
