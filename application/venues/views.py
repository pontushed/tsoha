from application import app, db
from flask import render_template, request, redirect, url_for
from application.venues.models import Venue
from application.events.models import Event
from application.venues.forms import VenueForm
from flask_login import login_required


@app.route("/venues/", methods=["GET"])
def venues_index():
    return render_template("venues/list.html", venues=Venue.query.all())


@app.route("/venues/new/")
@login_required
def venues_form():
    return render_template(
        "venues/data.html", form=VenueForm(), action="Add", data_type="a new venue"
    )


@app.route("/venues/<venue_id>", methods=["GET"])
@login_required
def venues_edit(venue_id):
    v = Venue.query.get(venue_id)
    return render_template(
        "venues/data.html",
        form=VenueForm(obj=v),
        action="Edit",
        data_type=v.name,
        id=v.id,
    )


@app.route("/venues/delete/<venue_id>", methods=["POST"])
@login_required
def venues_delete(venue_id):
    Event.query.filter_by(venue_id=venue_id).delete()
    v = Venue.query.get(venue_id)
    db.session.delete(v)
    db.session().commit()
    return redirect(url_for("venues_index"))


@app.route("/venues/", methods=["POST"])
@login_required
def venues_create():
    form = VenueForm(request.form)
    if not form.validate():
        return render_template(
            "venues/data.html", form=form, action="Add", data_type="a new venue"
        )
    v = Venue(form.name.data, form.location.data)

    db.session().add(v)
    db.session().commit()

    return redirect(url_for("venues_index"))


@app.route("/venues/<venue_id>", methods=["POST"])
@login_required
def venues_update(venue_id):
    form = VenueForm(request.form)
    v = Venue.query.get(venue_id)
    if not form.validate():
        return render_template(
            "venues/data.html", form=form, action="Edit", data_type=v.name, id=v.id,
        )
    v.name = form.name.data
    v.location = form.location.data
    db.session().commit()

    return redirect(url_for("venues_index"))
