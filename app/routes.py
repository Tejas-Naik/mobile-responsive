from logging import Formatter
from flask import render_template, flash, redirect, url_for
from flask.helpers import url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(Phone_Number=form.phone_number.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Phone number or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user = User(Phone_Number=form.phone_number.data)
        user.set_password(form.password.data)
        db.session.add('user')
        db.session.commit()
        flash('Congratulations, You are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title ='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

    