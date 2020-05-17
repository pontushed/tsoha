from application import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    post_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    comment = db.Column(db.Text)
