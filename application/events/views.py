from application import app, db
from flask import render_template, request, redirect, url_for
from application.events.models import Event, Comment
from application.events.forms import EventForm, CommentForm
from application.venues.models import Venue
from application.venues.forms import VenueForm
from application.auth.models import User
from flask_login import login_required, current_user
from sqlalchemy import text


@app.route("/events/", methods=["GET"])
def events_index():
    myevents = None
    if current_user.is_authenticated:
        myevents = User.query.get(current_user.id).events
        myevents = [e.id for e in myevents]
    return render_template(
        "events/list.html", events=Event.list_events(), myevents=myevents
    )


@app.route("/events/new/")
@login_required
def events_form():
    venueChoices = [
        (v.id, (v.name + " (" + v.location + ")")) for v in Venue.query.all()
    ]
    venueChoices.append((-1, "I will create a new venue"))
    eventForm = EventForm()
    eventForm.venue.choices = venueChoices
    return render_template(
        "events/data.html", form=eventForm, action="Organize", data_type="a new event",
    )


@app.route("/events/", methods=["POST"])
@login_required
def events_create():
    form = EventForm(request.form)
    venueChoices = [
        (v.id, (v.name + " (" + v.location + ")")) for v in Venue.query.all()
    ]
    venueChoices.append((-1, "I will create a new venue"))
    form.venue.choices = venueChoices
    if not form.validate():
        return render_template(
            "events/data.html", form=form, action="Organize", data_type="a new event",
        )

    venue_id = form.venue.data
    if form.venue.data == -1:
        v = Venue(form.new_venue_name.data, form.new_venue_location.data)
        db.session().add(v)
        db.session().commit()
        venue_id = v.id

    e = Event(
        admin_id=current_user.id,
        name=form.name.data,
        info=form.info.data,
        venue_id=venue_id,
        start_time=form.start_time.data,
        end_time=form.end_time.data,
    )

    db.session().add(e)
    db.session().commit()

    return redirect(url_for("events_index"))


@app.route("/events/<event_id>", methods=["GET"])
def events_single(event_id):
    commentForm = CommentForm()
    e = Event.query.get(event_id)
    v = Venue.query.get(e.venue_id)
    organizer = User.query.get(e.admin_id)
    comments = Event.get_event_comments(event_id)
    participants = Event.get_event_participants(event_id)
    return render_template(
        "events/single.html",
        event=e,
        venue=v,
        organizer=organizer,
        comments=comments,
        commentForm=commentForm,
        participants_list=participants,
    )


@app.route("/events/edit/<event_id>", methods=["GET"])
@login_required
def events_edit(event_id):
    e = Event.query.get(event_id)
    if e.admin_id != current_user.id:
        return redirect(url_for("events_index"))
    venueChoices = [
        (v.id, (v.name + " (" + v.location + ")")) for v in Venue.query.all()
    ]
    eventForm = EventForm(obj=e)
    eventForm.venue.choices = venueChoices
    return render_template(
        "events/data.html", form=eventForm, action="Edit", data_type=e.name, id=e.id,
    )


@app.route("/events/delete/<event_id>", methods=["POST"])
@login_required
def events_delete(event_id):
    e = Event.query.get(event_id)
    if e.admin_id == current_user.id or (
        "admin" in [role.name for role in current_user.roles]
    ):
        sql = text("DELETE FROM events_participants WHERE event_id=:event_id").params(
            event_id=event_id
        )
        db.engine.execute(sql)
        db.session.delete(e)
        db.session().commit()
    return redirect(url_for("events_index"))


@app.route("/events/edit/<event_id>", methods=["POST"])
@login_required
def events_update(event_id):
    form = EventForm(request.form)
    venueChoices = [
        (v.id, (v.name + " (" + v.location + ")")) for v in Venue.query.all()
    ]
    form.venue.choices = venueChoices
    e = Event.query.get(event_id)
    if e.admin_id != current_user.id:
        return redirect(url_for("events_index"))
    if not form.validate():
        return render_template(
            "events/data.html", form=form, action="Edit", data_type=e.name, id=e.id,
        )

    e.name = form.name.data
    e.info = form.info.data
    e.venue_id = form.venue.data
    e.start_time = form.start_time.data
    e.end_time = form.end_time.data
    db.session().commit()

    return redirect(url_for("events_index"))


@app.route("/events/<event_id>/join", methods=["POST"])
@login_required
def join_event(event_id):
    """ sql = text(
        "INSERT INTO events_participants (user_id, event_id) VALUES (:userid, :eventid)"
    ).params(userid=current_user.id, eventid=event_id)
    db.engine.execute(sql)"""
    user = User.query.get(current_user.id)
    event = Event.query.get(event_id)
    user.events.append(event)
    db.session.commit()
    if "frontpage=1" in request.url:
        return redirect(url_for("index"))
    return redirect(url_for("events_index"))


@app.route("/events/<event_id>/leave", methods=["POST"])
@login_required
def leave_event(event_id):
    """print(current_user.get_id(), "leaves event ", event_id)
    sql = text(
        "DELETE FROM events_participants WHERE user_id=:userid AND event_id=:eventid"
    ).params(userid=current_user.id, eventid=event_id)
    db.engine.execute(sql)"""
    user = User.query.get(current_user.id)
    event = Event.query.get(event_id)
    user.events.remove(event)
    db.session.commit()

    if "frontpage=1" in request.url:
        return redirect(url_for("index"))
    return redirect(url_for("events_index"))


@app.route("/events/<event_id>/comment", methods=["POST"])
@login_required
def events_add_comment(event_id):
    form = CommentForm(request.form)
    comment = Comment(
        author_id=current_user.id, event_id=event_id, comment=form.comment.data
    )
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("events_single", event_id=event_id))


@app.route("/events/<event_id>/comment/<comment_id>/delete", methods=["POST"])
@login_required
def comments_delete(event_id, comment_id):
    event = Event.query.get(event_id)
    comment = Comment.query.get(comment_id)
    if event.admin_id == current_user.id or (
        "admin" in [role.name for role in current_user.roles]
    ):
        db.session.delete(comment)
        db.session().commit()
    return redirect(url_for("events_single", event_id=event_id))
