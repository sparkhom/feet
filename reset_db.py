from feet import app
from feet.models import db, User, Event, Request
from datetime import datetime
from hashlib import sha1

ctx = app.test_request_context()
ctx.push()
db.drop_all()
db.create_all()
tim = User('tim', sha1('password').hexdigest(), 'got.ownage@gmail.com', 'La Jolla, CA', 32.868325, -117.224038, 'Tim', 'Kang')
db.session.add(tim)
db.session.commit()
bleh = Event(32.868325, -117.224038, 'La Jolla, CA', 'Test description', tim, datetime.utcnow()) 
db.session.add(bleh)
db.session.commit()
# ctx.pop()
