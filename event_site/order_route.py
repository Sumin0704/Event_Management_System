from flask import Blueprint, render_template, session, request, redirect, url_for
from .models import Event, Order, EventStatus, User
from flask_login import login_required, current_user
from .forms import OrderForm
from datetime import datetime
from . import db



mainbp = Blueprint("order", __name__, url_prefix="/order")

@mainbp.route("/place/<id>", methods = ['GET', 'POST'])
@login_required
def place(id):
    print("Method type: ", request.method)
    user = current_user
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + user.id)
    form = OrderForm()
    if form.validate_on_submit():
        order = Order( # from models
            order_numTickets = form.order_num_tickets.data,
            order_dateTime = datetime.now(),
            user_id=user.id,
            event_id=id,
        )
        db.session.add(order) # add the object to the db session
        db.session.commit() # commit to the database
        print("Successfully place new order", "success")
        return redirect(url_for("main.index")) # Always end with redirect when form is valid
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
