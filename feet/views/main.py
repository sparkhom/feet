from __future__ import absolute_import
from flask import Module, render_template, session, g, request, flash, redirect, url_for
from feet.models import db, User, Event, Request
from flaskext.wtf import Form, TextField, PasswordField, SubmitField, HiddenField, Required, Optional
from wtforms.ext.dateutil.fields import DateTimeField
from hashlib import sha1
from json import dumps, loads

main = Module(__name__)

class LoginForm(Form):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Login')

class PostForm(Form):
    description = TextField('I\'m looking for...', validators=[Required()])
    location = HiddenField(validators=[Required()])
    start_time = DateTimeField('Start Time')
    end_time = DateTimeField('End Time', validators=[Optional()])
    expire_time = DateTimeField('Expire Time', validators=[Optional()])
    submit = SubmitField('Look for others')

@main.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@main.route('/', methods=['GET','POST'])
def index():
    error = []
    send = None
    form = PostForm()
    if form.is_submitted():
        if form.validate():
            event = Event(form.location, form.description, g.user, form.start_time, form.end_time, form.expire_time) 
            try:
                db.session.add(event)
                db.session.commit()
            except sqlalchemy.exc.SQLAlchemyError:
                error.append('Something weird happened, try again!')
            if (len(error) > 0):
                send = { 'success' : 0, 'error' : error, 'validation' : validation }
            else:
                send = { 'success' : 1 }
        else:
            send = {'success' : 0, 'validation' : form.errors }
        return dumps(send)
    return render_template('main.html', form=form, events=Event.query.order_by(Event.created.desc()))

@main.route('/login', methods=['GET','POST'])
def login():
    if g.user is not None:
        return redirect(url_for('index'))
    error = []
    validation = []
    send = None
    form = LoginForm()
    if form.is_submitted():
        if form.validate():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or user.password != sha1(form.password.data).hexdigest():
                error.append('Username/password is incorrect.')
            else:
                session['user_id'] = user.id
            if (len(error) > 0):
                send = {'success' : 0, 'error' : error, 'validation' : validation}
            else:
                send = {'success' : 1}
        else:
            send = {'success' : 0, 'validation' : form.errors }
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
