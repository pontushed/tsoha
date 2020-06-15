from flask_wtf import FlaskForm
from wtforms import StringField, validators, ValidationError
from application.venues.models import Venue


class VenueForm(FlaskForm):
    name = StringField(
        "Venue name",
        [
            validators.Length(min=2, max=40),
            validators.InputRequired("Please enter a name."),
        ],
    )
    location = StringField(
        "Venue location",
        [
            validators.Length(min=2, max=144),
            validators.InputRequired("Please enter a location."),
        ],
    )

    class Meta:
        csrf = False

    def validate(self, extra_validators=None):
        res = super().validate(extra_validators=extra_validators)
        duplicateVenue = Venue.query.filter_by(
            name=self.name.data, location=self.location.data
        ).first()
        if duplicateVenue:
            self.name.errors.append("This Venue already exists.")
            self.location.errors.append("This Venue already exists.")
            return False
        return res
