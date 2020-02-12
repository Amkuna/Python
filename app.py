from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////tmp.test.db'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24))
    email = db.Column(db.String(80))
    password = db.Column(db.String(100))

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return True

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')

# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=["GET", "POST"])
def login():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     login_user(user)
    #
    #     flash("Logged in successfully")
    #
    #     next = request.args.get('next')
    #
    #     if not is_safe_url(next):
    #         return abort(400)
    #
    #     return redirect(next or url_for('index'))
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
