from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from application.venues.models import Venue


class EventForm(FlaskForm):
    name = StringField("Event name", [validators.Length(min=2)])
    info = StringField("Event info", [validators.Length(min=2)])
    venueChoices = [
        (v.id, (v.name + " (" + v.location + ")")) for v in Venue.query.all()
    ]
    venue = SelectField("Event venue", choices=venueChoices, coerce=int)

    class Meta:
        csrf = False
