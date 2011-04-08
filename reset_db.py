from feet import app
from feet.models import db, User, Event, Request
from datetime import datetime

ctx = app.test_request_context()
ctx.push()
db.drop_all()
db.create_all()
tim = User('tim', 'password', 'got.ownage@gmail.com', 'La Jolla, CA', 'Tim', 'Kang')
db.session.add(tim)
db.session.commit()
bleh = Event('La Jolla, CA', 'Test description', tim, datetime.utcnow()) 
db.session.add(bleh)
db.session.commit()
# ctx.pop()
