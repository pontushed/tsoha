from flask_wtf import FlaskForm
from wtforms import StringField, validators


class VenueForm(FlaskForm):
    name = StringField("Venue name", [validators.Length(min=2)])
    location = StringField("Venue location", [validators.Length(min=2)])

    class Meta:
        csrf = False
