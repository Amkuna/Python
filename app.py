from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)



class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        email = request.form["email"]
        password = request.form["password"]
        # remember = True if request.form["remember"] else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect(url_for("login"))

        return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first() #if returns a user, it's already registered

        if user:
            flash("Email already exists")
            return redirect(url_for("register"))

        new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("index"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
