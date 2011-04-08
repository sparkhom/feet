from flaskext.sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

event_members = db.Table('event_members',
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('event_id', db.Integer, db.ForeignKey('events.id'))
        )

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(256))
    email = db.Column(db.String(256))
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    location = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    website = db.Column(db.String(80))
    aim = db.Column(db.String(80))
    gtalk = db.Column(db.String(80))
    events = db.relationship('Event', secondary=event_members, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    created = db.Column(db.DateTime)

    def __init__(self, username, password, email, latitude, longitude, location, first_name=None, last_name=None, phone=None, website=None, aim=None, gtalk=None):
        self.username = username
        self.password = password
        self.email = email
        self.latitude = latitude
        self.longitude = longitude
        self.location = location
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.website = website
        self.aim = aim
        self.gtalk = gtalk
        self.created = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.username

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('requests', lazy='dynamic'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = db.relationship('Event', backref=db.backref('requests', lazy='dynamic'))
    message = db.Column(db.String(256))
    created = db.Column(db.DateTime)

    def __init__(self, user, event, message=None):
        self.user = user
        self.event = event
        self.message = message
        self.created = datetime.utcnow()

    def __repr__(self):
        return '<Request %r>' % self.id

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    location = db.Column(db.String(80))
    description = db.Column(db.String(160))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship('User', backref=db.backref('creator', lazy='dynamic'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    expire_time = db.Column(db.DateTime)
    created = db.Column(db.DateTime)

    def __init__(self, latitude, longitude, location, description, creator, start_time, end_time=None, expire_time=None):
        self.latitude = latitude
        self.longitude = longitude
        self.location = location
        self.description = description
        self.creator = creator
        self.start_time = start_time
        self.end_time = end_time
        self.expire_time = expire_time
        self.created = datetime.utcnow()

    def __repr__(self):
        return '<Event %r>' % self.description

'''class EventMember(db.Model):
    __tablename__ = 'eventmembers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('users',lazy='dynamic'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = db.relationship('Event', backref=db.backref('events',lazy='dynamic'))

    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id

    def __repr__(self):
        return '<EventMember %r>' % self.userid, self.event_id
        '''
