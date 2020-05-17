from application import app, db
from flask import render_template, request
from application.venues.models import Venue
from application.venues.forms import VenueForm


@app.route("/venues/", methods=["GET"])
def venues_index():
    return render_template("venues/list.html", venues=Venue.query.all())


@app.route("/venues/new/")
def venues_form():
    return render_template("venues/new.html", form=VenueForm())


@app.route("/venues/", methods=["POST"])
def venues_create():
    form = VenueForm(request.form)
    t = Venue(form.name.data, form.location.data)

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("venues_index"))
