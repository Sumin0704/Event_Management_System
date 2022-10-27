from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from .models import Event, Order, User
from flask_login import login_required, current_user
from .forms import OrderForm
from datetime import datetime
from . import db
from sqlalchemy import desc



mainbp = Blueprint("order", __name__, url_prefix="/order")

@mainbp.route("/place/<id>", methods = ['GET', 'POST'])
@login_required
def place(id):
    print("Method type: ", request.method)
    form = OrderForm()
    user=current_user
    if form.validate_on_submit():
        # we have a valid number of tickets need to check if it changes event status
        tickets_ordered = form.order_num_tickets.data # say 10
        # query avaliable tickets from event
        event = Event.query.filter_by(event_id=id).first()
        tickets_aval = event.event_TicketsAvailable # say 1000
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
            order_numTickets = form.order_num_tickets.data,
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
            return redirect(url_for('event.book', eventid=event.event_id)) 
        

    return redirect(url_for("event.show", id=id))



@mainbp.route("/history")
@login_required
def history():
    user=current_user
    # print("user ID ISSSSSSSSSS"+ str(user.id))
    orders = Order.query.filter_by(user_id=user.id) # user.id = 1, this is working
    # print(orders.event_id)
    # events = Event.query.filter_by(event_id=orders.event_id)
    # print(events)
    return render_template('history.html', orders=orders)#, events=events)

