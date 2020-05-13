from flask_login import UserMixin
from Auction import db, login_manager
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, InputRequired
from flask_wtf.file import FileField, FileRequired
from .helpers.categories import choices
from wtforms.fields import (StringField, SelectField, IntegerField, TimeField, TextAreaField)
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True) 
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    auctions = db.relationship('Auction',backref='user',lazy=True)
    offers = db.relationship("Offer", backref='user', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Auction(db.Model):
    __tablename__ = 'auctions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    offers = db.relationship('Offer', backref='auction', lazy=True)

    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    min_price = db.Column(db.Integer, nullable=False)
    auction_image = db.Column(db.String(256), nullable=False)
    end_day = db.Column(db.Date, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    views = db.Column(db.Integer, nullable=False)


class Offer(db.Model):
    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Offer: " + str(self.price)

class FinishedAuctions(db.Model):
    __tablename__ = "finishedauctions"

    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    offer = db.Column(db.Integer)

