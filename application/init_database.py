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
    Event.query.delete()
    Venue.query.delete()
    User.query.delete()
    db.session.commit()
    u = User(
        username="admin",
        full_name="Administrator",
        password="admin",
        email="admin@localhost",
    )
    db.session.add(u)
    v1 = Venue(name="Gurula", location="Exactum")
    db.session.add(v1)
    v2 = Venue(name="Klusteri", location="Leppäsuonkatu 12, Helsinki")
    db.session.add(v2)
    db.session.commit()

    e = Event(
        admin_id=u.id,
        name="Testitapahtuma",
        info="Testi",
        venue_id=v1.id,
        start_time=datetime.now() + timedelta(hours=2),
        end_time=datetime.now() + timedelta(hours=4),
    )
    db.session().add(e)
    e = Event(
        admin_id=u.id,
        name="Testitapahtuma2",
        info="Testi2",
        venue_id=v2.id,
        start_time=datetime.now() + timedelta(hours=2),
        end_time=datetime.now() + timedelta(hours=4),
    )
    db.session().add(e)
    db.session.commit()

    return redirect(url_for("index"))
