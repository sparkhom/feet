from __future__ import absolute_import
from flask import Flask
from feet.models import db, User, Event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'devkey'
db.init_app(app)

from feet.views.main import main
app.register_module(main)
