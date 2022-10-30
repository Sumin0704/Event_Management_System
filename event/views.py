from flask import Blueprint, render_template, session, request, redirect, url_for
from .models import Event
from flask_login import login_required, current_user

mainbp = Blueprint("main",__name__)


@mainbp.route("/")
def index():
    events = Event.query.filter(Event.event_Status.in_(('Open', 'Sold Out', 'Cancelled')))
    return render_template("index.html", events=events)

@mainbp.route("/myevents")
@login_required
def myEvents():
    myevents = Event.query.filter_by(event_creator=current_user.id)
    return render_template('history.html',myevents=myevents)