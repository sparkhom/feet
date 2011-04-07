from feet import app
from feet.models import db, User, Event

ctx = app.test_request_context()
ctx.push()
db.create_all()
ctx.pop()
