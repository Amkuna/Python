from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from Auction.helpers.categories import choices

from flask_login import current_user
from Auction.models import User

class SelectCategoryForm(FlaskForm):
    category = SelectField('Category', choices=choices)
    submit = SubmitField('Search')


