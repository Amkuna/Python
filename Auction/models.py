from flask_login import UserMixin
from Auction import db
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, InputRequired
from flask_wtf.file import FileField, FileRequired
from .helpers.categories import choices
from wtforms.fields import (StringField, SelectField, IntegerField, TimeField, TextAreaField)

class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), validators=[DataRequired()])
    category = db.Column(db.String(80), choices=choices)
    description = db.Column(db.String(80), validators=[DataRequired()])
    country = db.Column(db.String(80), validators=[DataRequired()])
    min_price = db.Column(db.Integer)
    auction_image = db.Column(db.String(256), validators=[DataRequired()])
    end_day = db.Column(db.Date, validators=[DataRequired()])
    end_time = db.Column(db.Time, validators=[DataRequired()])
    offers = db.relationship('Offer', backref='auction')
    views = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))
    name = db.Column(db.String(32))

class Offer(db.Model):
    __tablename__ = "Offer"
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'), nullable=False)
    user_id = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)