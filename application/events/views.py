from application import app, db
from flask import render_template, request, redirect, url_for
from application.events.models import Event
from application.events.forms import EventForm
from application.venues.models import Venue
from flask_login import login_required, current_user
from datetime import datetime, timedelta


@app.route("/events/", methods=["GET"])
def events_index():
    return render_template("events/list.html", events=Event.list_events())


@app.route("/events/new/")
@login_required
def events_form():
    return render_template(
        "events/data.html",
        form=EventForm(),
        action="Organize",
        data_type="a new event",
    )


@app.route("/events/", methods=["POST"])
@login_required
def events_create():
    form = EventForm(request.form)
    if not form.validate():
        return render_template(
            "events/data.html", form=form, action="Organize", data_type="a new event"
        )
    e = Event(
        admin_id=current_user.id,
        name=form.name.data,
        info=form.info.data,
        venue_id=form.venue.data,
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=2),
    )

    db.session().add(e)
    db.session().commit()

    return redirect(url_for("events_index"))


@app.route("/events/<event_id>", methods=["GET"])
@login_required
def events_edit(event_id):
    e = Event.query.get(event_id)
    return render_template(
        "events/data.html",
        form=EventForm(obj=e),
        action="Edit",
        data_type=e.name,
        id=e.id,
    )


@app.route("/events/delete/<event_id>", methods=["POST"])
@login_required
def events_delete(event_id):
    e = Event.query.get(event_id)
    db.session.delete(e)
    db.session().commit()
    return redirect(url_for("events_index"))


@app.route("/events/<event_id>", methods=["POST"])
@login_required
def events_update(event_id):
    form = EventForm(request.form)
    e = Event.query.get(event_id)
    if not form.validate():
        return render_template(
            "events/data.html", form=form, action="Edit", data_type=e.name, id=e.id,
        )

    e.name = form.name.data
    e.info = form.info.data
    e.venue_id = form.venue.data
    e.start_time = datetime.now()
    e.end_time = datetime.now() + timedelta(hours=2)
    db.session().commit()

    return redirect(url_for("events_index"))
