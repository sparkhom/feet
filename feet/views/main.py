from __future__ import absolute_import
from flask import Module, render_template, session, g, request, flash, redirect, url_for
from feet.models import db, User, Event, Request
from flaskext.wtf import Form, TextField, PasswordField, SubmitField
from hashlib import sha1
from json import dumps, loads

main = Module(__name__)

class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')

@main.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@main.route('/')
def index():
    return render_template('main.html', events=Event.query.order_by(Event.created.desc()))

@main.route('/login', methods=['GET','POST'])
def login():
    if g.user is not None:
        return redirect(url_for('index'))
    error = []
    send = None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or user.password != sha1(form.password.data).hexdigest():
            error.append('Username/password is incorrect.')
        else:
            session['user_id'] = user.id
        if (len(error) > 0):
            send = {'success' : 0, 'error' : error}
        else:
            send = {'success' : 1}
        return dumps(send)
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    if g.user is None:
        flash('You are not logged in.')
        return redirect(url_for('index'))
    del session['user_id']
    flash('You have now been logged out.')
    return redirect(url_for('index'))
