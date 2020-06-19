from application import db
from sqlalchemy import text


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    post_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    comment = db.Column(db.Text)

    def __init__(self, **kwargs):
        self.event_id = kwargs["event_id"]
        self.author_id = kwargs["author_id"]
        self.comment = kwargs["comment"]


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    name = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    info = db.Column(db.Text)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime, index=True)
    comments = db.relationship("Comment", cascade="delete")

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

    @staticmethod
    def get_event_comments(event_id):
        sql = text(
            """SELECT t1.id, t1.comment as comment, t2.full_name as author, t1.post_time as post_time from comments t1
            LEFT JOIN account t2 ON t2.id=t1.author_id
            WHERE t1.event_id=:event_id"""
        ).params(event_id=event_id)
        return db.engine.execute(sql)

    @staticmethod
    def get_event_participants(event_id):
        sql = text(
            """SELECT t1.full_name FROM account t1
            INNER JOIN events_participants t2 ON t2.user_id=t1.id
            WHERE t2.event_id=:event_id"""
        ).params(event_id=event_id)
        return db.engine.execute(sql)

    @staticmethod
    def event_summary():
        stmt = text(
            """
            WITH t4 AS (
                SELECT t1.*, count(t2.user_id) participants FROM event t1
                INNER JOIN events_participants t2
                ON t2.event_id=t1.id
                GROUP BY t1.id
            )
            SELECT t3.name venue_name, t3.location venue_location, t4.*, account.full_name as organizer
            FROM venue t3 LEFT JOIN t4 ON t4.venue_id = t3.id
            INNER JOIN account ON t4.admin_id=account.id
            WHERE t4.end_time > date('now')
        """
        )
        return db.engine.execute(stmt)
