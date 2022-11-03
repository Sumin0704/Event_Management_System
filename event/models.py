# Create the table of DB
from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    user_address = db.Column(db.String(255), nullable=True) # to do
    user_phone = db.Column(db.String(255), unique=True, nullable=True) # to do
    user_email_address = db.Column(db.String(100), index=True, unique=True, nullable=False)
    user_password_hash = db.Column(db.String(255), nullable=False)
    

    # Adding the Foreign key
    comments = db.relationship("Comment", backref="user") # means I can do user.comments to get all comments for a user
    events = db.relationship('Event', backref='user')
    # bookings = db.relationship('Bookings', backref='user')

class Event(db.Model):
    __tablename__ = "events"
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(80), nullable=False)
    event_type = db.Column(db.String(10), nullable=False)
    event_location = db.Column(db.String(200), nullable=False)
    event_rating = db.Column(db.String(200), nullable=False)
    event_description = db.Column(db.String(500), index=True, nullable=False)
    event_image = db.Column(db.String(200), nullable=False)
    event_StartDateTime = db.Column(db.DateTime, nullable=False) # do this
    event_EndDateTime = db.Column(db.DateTime, nullable=False) # do this
    event_TicketPrice = db.Column(db.String(200), nullable=False)
    event_TicketsAvailable = db.Column(db.Integer, nullable=False) # do this
    event_Status = db.Column(db.String(200), nullable=False)
    
    # Adding the Foreign key
    event_creator = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship("Comment", backref="event") # means I can do event.comments to get all comments on an event

    def __repr__(self):
        return "Name: {}".format(self.event_name)


class Comment(db.Model):
    __tablename__ = "comments"
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(500))
    comment_created_at = db.Column(db.DateTime, default=datetime.now())

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))

    def __repr__(self):
        return "Comment: {}".format(self.text)

class Order(db.Model):
    __tablename__ = "orders"
    order_RefNumber = db.Column(db.Integer, primary_key=True)
    # order_totalValue = db.Column(db.Integer)
    order_numTickets = db.Column(db.Integer)
    order_dateTime = db.Column(db.DateTime, default=datetime.now())

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))
