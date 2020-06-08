from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    DateTimeField,
    validators,
    ValidationError,
)
from datetime import datetime as dt


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
            validators.Length(min=2, max=40),
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
        return result
