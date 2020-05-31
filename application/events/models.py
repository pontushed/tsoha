from application import db
from sqlalchemy import text


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    name = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    info = db.Column(db.Text)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        self.admin_id = kwargs["admin_id"]
        self.name = kwargs["name"]
        self.info = kwargs["info"]
        self.venue_id = kwargs["venue_id"]
        self.start_time = kwargs["start_time"]
        self.end_time = kwargs["end_time"]

    @staticmethod
    def list_events():
        sql = text(
            """SELECT t1.*, t2.full_name AS organizer, t3.name AS venue_name, t3.location AS venue_location
        FROM event t1
        INNER JOIN account t2 ON t1.admin_id=t2.id
        INNER JOIN venue t3 ON t1.venue_id=t3.id
        WHERE t1.end_time > date('now')"""
        )
        return db.engine.execute(sql)
