from __future__ import absolute_import
from flask import Module, render_template
from feet.models import db, User, Event

main = Module(__name__)

@main.route('/')
def index():
    return render_template('show_entries.html', entries=Event.query.order_by(Event.description.desc()).all())
