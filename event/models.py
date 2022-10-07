# # Create the table of DB
# from . import db
# from datetime import datetime


# class User(db.Model):
#     __tablename__ = "user"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), index=True, unique=True, nullable=False)
#     email_address = db.Column(db.String(100), index=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)

#     # Adding the Foreign key
#     comment = db.relationship("Comment", backref="user")


# class Event(db.Model):
#     __tablename__ = "evnet"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     description = db.Column(db.String(500), index=True, nullable=False)
#     image = db.Column(db.String(400), nullable=False)
#     currency = db.Column(db.String(3), nullable=False)

#     # Adding the Foreign key
#     comment = db.relationship("Comment", backref="event")

#     def __repr__(self):
#         return "Name: {}".format(self.name)


# class Comment(db.Model):
#     __tablename__ = "comment"
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(500))
#     description = db.Column(db.DateTime, default=datetime.now())
#     # Foreign keys
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     destination_id = db.Column(db.Integer, db.ForeignKey("destination.id"))

#     def __repr__(self):
#         return "Comment: {}".format(self.text)



# Event Class
class Event:
    def __init__(self, name, image, date, time, status, price, location, rating, description):
        self.name = name
        self.image = image
        self.date = date
        self.time = time
        self.status= status
        self.price = price
        self.location = location
        self.rating = rating
        self.description = description
        self.comments = list()

    def add_comment(self, comment):
        self.comments.append(comment)

# Comment Class
class Comment:
    def __init__(self, user, text, created_at):
        self.user = user
        self.text = text
        self.created_at = created_at

    def __repr__(self):
        str = 'User {0}, \n Text {1}'
        str.format(self.user, self.text)
        return str