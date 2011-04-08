from feet import app
from feet.models import db, User, Event, Request
from datetime import datetime

ctx = app.test_request_context()
ctx.push()
# ctx.pop()
