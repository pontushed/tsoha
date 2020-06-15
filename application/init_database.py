from application import app, db, user_datastore
from application.auth.models import User, Role
from application.events.models import Event
from application.venues.models import Venue
from datetime import datetime, timedelta
from flask import url_for, redirect

# Create a user and a couple of venues and events to test with.
@app.route("/init")
def create_user():
    if User.query.count() == 0:
        Event.query.delete()
        Venue.query.delete()
        User.query.delete()
        Role.query.delete()
        db.session.commit()

        r = Role(name="admin", description="Administrator")
        db.session.add(r)

        u = User(
            username="admin",
            full_name="Administrator",
            password="admin",
            email="admin@localhost",
        )
        u.roles.append(r)
        db.session.add(u)
        u2 = User(
            username="basic",
            full_name="Basic User",
            password="basic",
            email="basic@localhost",
        )
        db.session.add(u2)
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
