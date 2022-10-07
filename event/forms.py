from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class EventForm(FlaskForm):
  name = StringField("Evnet Name", validators=[InputRequired()])
  # adding two validators, one to ensure input is entered and other to check if the
  # description meets the length requirements
  type = StringField("Event Type", validators=[InputRequired()])
  location = StringField("Location", validators=[InputRequired()])
  rating = StringField("Rating", validators=[InputRequired()])
  description = TextAreaField("Description", validators=[InputRequired()])
  image = TextAreaField("Image", validators=[InputRequired()])
  price = StringField("Price", validators=[InputRequired()])
  submit = SubmitField("Create")

class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Post')