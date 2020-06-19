from application import db
from application.events.models import Event
from sqlalchemy import text


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )
    name = db.Column(db.String(144), nullable=False)
    location = db.Column(db.String(144), nullable=False)
    events = db.relationship("Event", backref="event")

    __table_args__ = (db.UniqueConstraint("name", "location"),)

    def __init__(self, name, location):
        self.name = name
        self.location = location

    @staticmethod
    def venue_summary():
        sql = text(
            """
        SELECT venue.id, venue.name, venue.location, count(*) AS events FROM venue
        LEFT JOIN event ON venue.id=event.venue_id GROUP BY venue.name ORDER BY venue.name
        """
        )
        return db.engine.execute(sql)
