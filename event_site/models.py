# Create the table of DB
from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    user_email_address = db.Column(db.String(100), index=True, unique=True, nullable=False)
    user_password_hash = db.Column(db.String(255), nullable=False)
    user_address = db.Column(db.String(255), nullable=True) # to do
    user_phone = db.Column(db.String(255), unique=True, nullable=True) # to do

    # Adding the Foreign key
    comments = db.relationship("Comment", backref="user") # means I can do user.comments to get all comments for a user


class Event(db.Model):
    __tablename__ = "events"
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(80), nullable=False)
    event_type = db.Column(db.String(10), nullable=False)
    event_location = db.Column(db.String(200), nullable=False)
    event_rating = db.Column(db.String(200), nullable=False)
    event_description = db.Column(db.String(500), index=True, nullable=False)
    event_image = db.Column(db.String(200), nullable=False)
    event_StartDate = db.Column(db.String(20), nullable=False) # do this
    event_StartTime = db.Column(db.String(20), nullable=False) # do this
    event_EndDate = db.Column(db.String(20), nullable=True) # do this
    event_EndTime = db.Column(db.String(20), nullable=True) # do this
    event_price = db.Column(db.String(10), nullable=True)
    event_TicketsAvaliable = db.Column(db.String(10), nullable=True) # do this

    # Adding the Foreign key
    comments = db.relationship("Comment", backref="event") # means I can do event.comments to get all comments on an event

    def __repr__(self):
        return "Name: {}".format(self.name)


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
    order_totalValue = db.Column(db.Integer)
    order_numTickets = db.Column(db.Integer)
    order_dateTime = db.Column(db.DateTime, default=datetime.now())
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))

class EventStatus(db.Model):
    __tablename__ = "event status"
    eventStatus_id = db.Column(db.Integer, primary_key=True)
    eventStatus_value = db.Column(db.String(500), nullable=True) # do this

    # Foreign keys
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))