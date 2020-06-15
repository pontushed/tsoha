from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    DateTimeField,
    validators,
    ValidationError,
)
from datetime import datetime as dt
from application.venues.models import Venue


class CommentForm(FlaskForm):
    comment = StringField(
        "Add a comment",
        [validators.InputRequired("Enter something"), validators.Length(min=2, max=80)],
    )

    class Meta:
        csrf = False


def check_datetimefield_format(form, field):
    if type(field.data) is not dt:
        raise ValidationError("Check format of date/time: DD.MM.YYYY HH:MM")


class EventForm(FlaskForm):

    name = StringField(
        "Event name",
        [
            validators.Length(min=2, max=80),
            validators.InputRequired("Please enter the event name."),
        ],
    )
    info = StringField(
        "Event info",
        [
            validators.Length(min=2, max=255),
            validators.InputRequired("Please enter some information."),
        ],
    )
    venue = SelectField("Event venue", coerce=int)
    new_venue_name = StringField("New venue name")
    new_venue_location = StringField("New venue location")
    start_time = DateTimeField(
        "Start time",
        validators=[
            validators.InputRequired("Please enter a valid date/time."),
            check_datetimefield_format,
        ],
        format="%d.%m.%Y %H:%M",
        render_kw={"placeholder": "DD.MM.YYYY HH:MM"},
    )
    end_time = DateTimeField(
        "End time",
        validators=[
            validators.InputRequired("Please enter a valid date/time."),
            check_datetimefield_format,
        ],
        format="%d.%m.%Y %H:%M",
        render_kw={"placeholder": "DD.MM.YYYY HH:MM"},
    )

    class Meta:
        csrf = False

    def validate(self, extra_validators=None):
        result = super().validate(extra_validators=extra_validators)
        if type(self.start_time.data) is dt and type(self.end_time.data) is dt:
            if self.start_time.data < dt.now():
                self.start_time.errors.append("Event cannot start in the past")
                return False
            if self.end_time.data < dt.now():
                self.end_time.errors.append("Event cannot end in the past")
                return False
            if self.end_time.data < self.start_time.data:
                self.end_time.errors.append("Event cannot end before it starts")
                return False
        if self.venue.data == -1:
            name_length = len(self.new_venue_name.data)
            location_length = len(self.new_venue_location.data)
            if name_length < 2 or name_length > 40:
                self.new_venue_name.errors.append("Length should be: min=2, max=40")
                return False
            if name_length < 2 or name_length > 144:
                self.new_venue_location.errors.append(
                    "Length should be: min=2, max=144"
                )
                return False
            duplicateVenue = Venue.query.filter_by(
                name=self.new_venue_name.data, location=self.new_venue_location.data
            ).first()
            if duplicateVenue:
                self.new_venue_name.errors.append("This Venue already exists.")
                self.new_venue_location.errors.append("This Venue already exists.")
                return False
        return result
