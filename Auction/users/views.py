from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from Auction.models import User
from Auction.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from Auction import db

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('main.index')

            return redirect(next)
        else:
            flash("Please check your credentials")

    return render_template('login.html', form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        if not form.email_in_use(field=form.email.data):
            user = User(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data
                )
            db.session.add(user)
            db.session.commit()
            
            return redirect(url_for('users.login'))
        
        form.errors['email'] = ['This email is already in use!']

    return render_template('register.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))