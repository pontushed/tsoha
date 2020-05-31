from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateTimeField, validators, ValidationError
from application.venues.models import Venue
from datetime import datetime as dt


class EventForm(FlaskForm):
    name = StringField("Event name", [validators.Length(min=2)])
    info = StringField("Event info", [validators.Length(min=2)])
    venueChoices = [
        (v.id, (v.name + " (" + v.location + ")")) for v in Venue.query.all()
    ]
    venue = SelectField("Event venue", choices=venueChoices, coerce=int)
    start_time = DateTimeField(
        "Start time",
        format="%Y-%m-%d %H:%M",
        render_kw={"placeholder": "YYYY-MM-DD HH:MM"},
    )
    end_time = DateTimeField(
        "End time",
        format="%Y-%m-%d %H:%M",
        render_kw={"placeholder": "YYYY-MM-DD HH:MM"},
    )

    class Meta:
        csrf = False

    def validate_start_time(self, start_time):
        if start_time.data < dt.now():
            raise ValidationError("Event cannot start in the past")

    def validate_end_time(self, end_time):
        if end_time.data < dt.now():
            raise ValidationError("Event cannot start in the past")
        if end_time.data < self.start_time.data:
            raise ValidationError("Event cannot end before it starts")
