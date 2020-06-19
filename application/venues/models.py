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
            WITH t2 AS (
                SELECT venue.id, count(*) as events FROM venue
                LEFT JOIN event ON venue.id=event.venue_id GROUP BY venue.id
            )
            SELECT venue.id, venue.name, venue.location, t2.events AS events FROM venue
            LEFT JOIN t2 ON venue.id=t2.id ORDER BY venue.name
            """
        )
        return db.engine.execute(sql)
