from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from Auction.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=64)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=128), EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email=field).first():
            raise ValidationError("Your email has been already registered!")

    def check_username(self, field):
        if User.query.filter_by(username=field).first():
            raise ValidationError("Your username has been already registered!")

class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Update')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been already registered!")

        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Your username has been already registered!")

