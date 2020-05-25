from application import db


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
