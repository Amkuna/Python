from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FileField, TextAreaField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from Auction.helpers.categories import choices as categoryChoices
from Auction.helpers.countries import choices as countryChoices
from flask_login import current_user
from Auction.models import User

class AddAuctionForm(FlaskForm):
    name = StringField('Auction Name', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices=categoryChoices)
    description = TextAreaField("Description")
    country = SelectField("Country", validators=[DataRequired()], choices=countryChoices)
    min_price = IntegerField("Minimum Price", validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    end_day = DateField("End Day", validators=[DataRequired()])
    end_time = TimeField("End Time", validators=[DataRequired()])

    submit = SubmitField('Add Auction')

class EditAuctionForm(FlaskForm):
    name = StringField('Auction Name', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices=categoryChoices)
    description = TextAreaField("Description")
    country = SelectField("Country", validators=[DataRequired()], choices=countryChoices)
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Submit Changes')


