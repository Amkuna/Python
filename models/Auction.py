from .. import db

class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow)
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    title = db.Column(db.String)
