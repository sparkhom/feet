from __future__ import absolute_import
from flask import Module, render_template, session, g, request, flash, redirect, url_for
from feet.models import db, User, Event, Request
from flaskext.wtf import Form, TextField, PasswordField, SubmitField, HiddenField, Required, Optional, Email, Length, URL
from wtforms.ext.dateutil.fields import DateTimeField
from hashlib import sha1
from json import dumps, loads

main = Module(__name__)

class RegisterForm(Form):
    username = TextField('Username', validators=[Required(),Length(max=80)])
    password = PasswordField('Password', validators=[Required()])
    email = TextField('Email', validators=[Required(),Email(),Length(max=256)])
    latitude = HiddenField(validators=[Required()])
    longitude = HiddenField(validators=[Required()])
    location = HiddenField(validators=[Required(),Length(256)])
    first_name = TextField('First Name',validators=[Length(max=80)])
    last_name = TextField('Last Name',validators=[Length(max=80)])
    phone = TextField('Phone',validators=[Length(max=80)])
    website = TextField('Website', validators=[Optional(),URL(),Length(max=80)])
    aim = TextField('AIM',validators=[Length(max=80)])
    gtalk = TextField('Google Talk',validators=[Length(max=80)])
    submit = SubmitField('Register')

class LoginForm(Form):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Login')

class PostForm(Form):
    description = TextField('I\'m looking for...', validators=[Required()])
    latitude = HiddenField(validators=[Required()])
    longitude = HiddenField(validators=[Required()])
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

@main.route('/register', methods=['GET','POST'])
def register():
    error = []
    send = None
    form = RegisterForm()
    if g.user is not None:
        flash('You are already registered.')
        return redirect(url_for('index'))
    if form.is_submitted():
        if form.validate():
            if User.query.filter_by(username=form.username.data).count() > 0:
                error.append('There is already a user by that name.')
            else:
                user = User(form.username.data, sha1(form.password.data).hexdigest(), form.email.data, form.latitude.data, form.longitude.data, form.location.data, form.first_name.data, form.last_name.data, form.phone.data, form.website.data, form.aim.data, form.gtalk.data)
                try:
                    db.session.add(user)
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
    return render_template('register.html', form=form)

@main.route('/', methods=['GET','POST'])
def index():
    error = []
    send = None
    form = PostForm()
    if form.is_submitted():
        if g.user is None:
            flash('You must be logged in to do that.')
            return redirect(url_for('login'))
        if form.validate():
            event = Event(form.latitude.data, form.longitude.data, form.location.data, form.description.data, g.user, form.start_time.data, form.end_time.data, form.expire_time.data) 
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
