from sqlalchemy import DateTime

from Auction import db

class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    category = db.Column(db.String(80))
    description = db.Column(db.String(80))
    country = db.Column(db.String(80))
    min_price = db.Column(db.Integer)
    auction_image = db.Column(db.String(256))
    end_day = db.Column(db.Date)
    end_time = db.Column(db.Time)
    offers = db.relationship('Offer', backref='auction')
    views = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
