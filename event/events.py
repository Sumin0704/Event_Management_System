from flask import Blueprint, render_template, session, request, redirect, url_for
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename

mainbp = Blueprint("event", __name__, url_prefix="/events")

@mainbp.route("/<id>")
def show(id):
    # event = get_event()
    # brazil = get_destination()
    commentForm = CommentForm()
    event = Event.query.filter_by(id=id).first()
    return render_template(
        "detail.html", event=event, form=commentForm
    )

# def get_event():
#     tennis = Event("QLD Open 2022 Tennis", "hello.jpg", " Sat, 22 Oct", "5:00 – 11:30 pm", "Open(8tickets left)", "13.50(Aud)", "Kedron-Wavell Services Club 21 Kittyhawk Dr, Chermside QLD", "3.8/5.0",
#     "Festival will held")
#     comment1 = Comment("Sumin", "I like to go there agian", "12:00:00")
#     comment2 = Comment("Jenny", "It's dangerous", "12:05:10")
#     tennis.add_comment(comment1)
#     tennis.add_comment(comment2)
#     return tennis

# Create the Sport event route
@mainbp.route("/create", methods=["GET"])
def create():
    print("Method type: ", request.method)
    form = EventForm()
    return render_template("create_form.html", form=form)

@mainbp.route("/create", methods=["POST"])
def createFormSubmission():
    form = EventForm()
    db_file_path = check_upload_file(form)
    if form.validate_on_submit():
        destination = Event(
            name=form.name.data,
            type=form.type.data,
            location=form.location.data,
            rating=form.rating.data,
            description=form.description.data,
            image=db_file_path,
            price=form.price.data,   
        )
        # add the object to the db session
        db.session.add(destination)
        # commit to the database
        db.session.commit()
        print("Successfully created new travel event", "success")
        # Always end with redirect when form is valid
        return redirect(url_for("event.create"))

@mainbp.route("/<id>/comment", methods=["POST"])
def comment(id):
    # here the form is created  form = CommentForm()
    commentForm = CommentForm()
    # get the event object associated to the page and the comment
    event_obj = Event.query.filter_by(id=id).first()
    if commentForm.validate_on_submit():  # this is true only in case of POST method
        comment = Comment(text=commentForm.text.data, event=event_obj)
        db.session.add(comment)
        db.session.commit()
    # notice the signature of url_for
    return redirect(url_for("evnet.show", id=1))

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
