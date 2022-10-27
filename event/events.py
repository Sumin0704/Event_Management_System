from flask import Blueprint, render_template, session, request, redirect, url_for
from .models import Event, Comment
from .forms import EventForm, CommentForm, OrderForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime

mainbp = Blueprint("event", __name__, url_prefix="/events")

@mainbp.route("/<id>")
def show(id):
    commentForm = CommentForm()
    orderForm = OrderForm()
    event = Event.query.filter_by(event_id=id).first()
    return render_template(
        "detail.html", event=event, commentForm=commentForm, orderForm=orderForm
    )

# Create the Sport event route
@mainbp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    print("Method type: ", request.method)
    form = EventForm()
    if form.validate_on_submit():
        # call the function that checks and returns image
        db_file_path = check_upload_file(form)
        event = Event(
            event_name = form.name.data,
            event_type = form.type.data,
            event_location = form.location.data,
            event_rating = form.rating.data,
            event_description = form.description.data,
            event_image = db_file_path,
            event_StartDateTime = form.startDateTime.data,
            event_EndDateTime = form.endDateTime.data,
            # event_price = form.price.data,
            event_TicketsAvailable = form.ticketsAvailable.data,
            user=current_user
        )
        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()
        print("Successfully created new event", "success")
        # Always end with redirect when form is valid
        return redirect(url_for("main.index"))
    return render_template("create_form.html", form=form)

@mainbp.route("/<id>/comment", methods = ['GET', 'POST'])
@login_required
def comment(id):
    print(id)
    # here the form is created  form = CommentForm()
    commentForm = CommentForm()
    # get the event object associated to the page and the comment
    event_obj = Event.query.filter_by(event_id=id).first()
    if commentForm.validate_on_submit(): # this is true only in case of POST method
        comment = Comment(
            comment_text=commentForm.text.data,
            comment_created_at = datetime.now(),
            event=event_obj,
            user=current_user,
        )
        db.session.add(comment)
        db.session.commit()
    # notice the signature of url_for
    return redirect(url_for("event.show", id=id))

def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    filename = fp.filename
    # get the current path of the module file… store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(BASE_PATH, "static/img", secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = "/static/img/" + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path


@mainbp.route("/book/<eventid>", methods=["GET", "POST"])
@login_required
def book(eventid):
    orderForm = OrderForm()
    commentForm = CommentForm()
    eventinfo = Event.query.filter_by(event_id=eventid).first()
    return render_template('book_tickets.html',eventinfo=eventinfo, orderForm=orderForm, commentForm=commentForm)