from multiprocessing import synchronize
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from .models import Event, Comment, Order
from .forms import EventForm, CommentForm, OrderForm, EditEventForm, LoginForm
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
    # status = event.event_Status
    # if status == "Cancelled":
    #     flash("This event has been cancelled and can no longer be booked")
    # elif status == "Open"
    #     if 
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
            event_TicketPrice = form.price.data,
            event_Status = form.status.data,
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


@mainbp.route("/edit/<id>", methods=["GET","POST"])
@login_required # Need to make this also only the owner
def editEvent(id):
    print("Method type: ", request.method)
    preFilledData = Event.query.filter_by(event_id=id).first()
    # here need to make sure the logged in user is same as preFilledData.event_creator
    # if not logged in as creator return auth.login
    # else continue with everything below
    if preFilledData.event_creator != current_user.id:
        flash("cannot edit an event that you did not create")
        return redirect(url_for("auth.login"))
    else:
        form = EditEventForm()
        if form.validate_on_submit():
            # If a new image was supplied, update it (need to check since it is not mandatory
            # to supply an image on the EditEventForm, therefore check_upload_file would write an
            # empty string to the event's image database column)
            if (form.image.data is not None): # they have chosen to change the image
                # call the function that checks and returns image
                db_file_path = check_upload_file(form)
                Event.query.filter_by(event_id=id).update(
                    {'event_image': db_file_path}, synchronize_session='evaluate'
                )
            # update rest of event separately to the image
            Event.query.filter_by(event_id=id).update(
                {'event_name':form.name.data,
                'event_type':form.type.data,
                'event_location':form.location.data,
                'event_rating':form.rating.data,
                'event_description':form.description.data,
                'event_StartDateTime':form.startDateTime.data,
                'event_EndDateTime':form.endDateTime.data,
                'event_TicketPrice':form.price.data,
                'event_Status':form.status.data,
                'event_TicketsAvailable':form.ticketsAvailable.data}, synchronize_session='evaluate'
            )
            print(form.ticketsAvailable.data)
            db.session.commit()
            print("Successfully created new event", "success")
            # Always end with redirect when form is valid
            return redirect(url_for("main.myEvents"))
        else:
            form.name.data = preFilledData.event_name
            form.type.data = preFilledData.event_type
            form.location.data = preFilledData.event_location
            form.rating.data = preFilledData.event_rating
            form.description.data = preFilledData.event_description
            form.startDateTime.data = preFilledData.event_StartDateTime
            form.endDateTime.data = preFilledData.event_EndDateTime
            form.price.data = preFilledData.event_TicketPrice
            form.status.data = preFilledData.event_Status
            form.ticketsAvailable.data = preFilledData.event_TicketsAvailable
        return render_template("editevent.html", form=form)

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


@mainbp.route("/<id>/book", methods=["GET", "POST"])
@login_required
def book(id):
    orderForm = OrderForm()
    user=current_user
    

    if orderForm.validate_on_submit():
        # we have a valid number of tickets need to check if it changes event status
        tickets_ordered = orderForm.order_num_tickets.data # say 10
        # query avaliable tickets from event
        event = Event.query.filter_by(event_id=id).first()
        tickets_aval = event.event_TicketsAvailable # say 1000
        if event.event_Status == "Open":
            # check that ordered tickets are less than or equal avaliable
            if tickets_ordered <= tickets_aval: # 10 <= 1000
                # can place order
                new_tickets_aval = tickets_aval - tickets_ordered
                # first it to update event in db with new avaliable tickets
                event.event_TicketsAvailable = new_tickets_aval
                if tickets_ordered == tickets_aval:
                    # print("got here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    # print(tickets_ordered)
                    # print(tickets_aval)
                    event.event_Status = "Sold Out"
                    db.session.commit()
                db.session.commit()

                # place order, give ref
                order = Order( # from models
                order_numTickets = orderForm.order_num_tickets.data,
                order_dateTime = datetime.now(),
                user_id=user.id,
                event_id=id,
                )
                db.session.add(order) # add the object to the db session
                db.session.commit() # commit to the database
                print("Successfully place new order", "success")
                flash("Order for " + str(order.order_numTickets) + " tickets placed successfully Ref: " + str(order.order_RefNumber)) #orderRef)
                return redirect(url_for("main.index")) # Always end with redirect when form is valid
            else: 
                # send message and redirect to same place order page with flashed message
                flash("Order Not Placed, there are only " + str(tickets_aval) + " tickets remaining")
                return redirect(url_for('event.show', id=event.event_id)) 
        else:
            flash("Order Not Placed, " + str(event.event_name)+  " is " + str(event.event_Status))
    return redirect(url_for("event.show", id=id))