from email.policy import default
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField,DateTimeLocalField, IntegerField, DecimalField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange


ALLOWED_FILE = {"PNG", "JPG", "JPEG", "png", "jpg", "jpeg"}
STATUS_CHOICES = [("Open", "Open"), ("Unpublished", "Unpublished"), ("Sold Out", "Sold Out"), ("Cancelled", "Cancelled")]
TYPE_CHOICES = [('Basketball', 'Basketball'), ('Boxing', 'Boxing'), ('Cricket', 'Cricket'), ('Golf', 'Golf'), ('Rugby', 'Rugby'), 
    ('Soccer', 'Soccer'), ('Tennis', 'Tennis'), ('Etc', 'Etc')]
class LoginForm(FlaskForm):
    name = StringField("User Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    user_address = StringField("User Address", validators=[InputRequired()])
    user_phone = StringField('User Phone' , validators=[InputRequired()])
    email_id = StringField(
        "Email Address", validators=[Email("Please enter a valid email")]
    )
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            EqualTo("confirm", message="Passwords should match"),
        ],
    )
    render_kw={'style':'font-size:150%'}
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")


class EventForm(FlaskForm):
  name = StringField("Event Name", validators=[InputRequired()])
  # adding two validators, one to ensure input is entered and other to check if the
  # description meets the length requirements
  type = SelectField("Event Type", choices=TYPE_CHOICES, validators=[InputRequired()])
  location = StringField("Location", validators=[InputRequired()])
  rating = StringField("Rating", validators=[InputRequired()])
  description = TextAreaField("Description", validators=[InputRequired()])
  image = FileField(
        "Destination Image",
        validators=[
            FileRequired(message="Must upload a photo"),
            FileAllowed(ALLOWED_FILE, message="Only supports png,jpg,JPG,PNG"),
        ],
    )
  startDateTime = DateTimeLocalField("Start Date and Time", format="%Y-%m-%dT%H:%M", validators=[InputRequired()])
  endDateTime = DateTimeLocalField("End Date and Time", format="%Y-%m-%dT%H:%M",validators=[InputRequired()])
  ticketsAvailable = IntegerField("Total Available Tickets",validators=[InputRequired(), NumberRange(min=0)])
  price = IntegerField("Individual Ticket Price", validators=[InputRequired(), NumberRange(min=0)])
  status = SelectField("Event Status", choices=STATUS_CHOICES, validators=[InputRequired()])
  submit = SubmitField("Create")

class EditEventForm(FlaskForm):
  name = StringField("Event Name", validators=[InputRequired()])
  # adding two validators, one to ensure input is entered and other to check if the
  # description meets the length requirements
  type = SelectField("Event Type", choices=TYPE_CHOICES, validators=[InputRequired()])
  location = StringField("Location", validators=[InputRequired()])
  rating = StringField("Rating", validators=[InputRequired()])
  description = TextAreaField("Description", validators=[InputRequired()])
  image = FileField(
        "Destination Image",
        validators=[
            FileAllowed(ALLOWED_FILE, message="Only supports png,jpg,JPG,PNG"),
        ],
    )
  startDateTime = DateTimeLocalField("Start Date and Time", format="%Y-%m-%dT%H:%M", validators=[InputRequired()])
  endDateTime = DateTimeLocalField("End Date and Time", format="%Y-%m-%dT%H:%M",validators=[InputRequired()])
  ticketsAvailable = IntegerField("Total Available Tickets",validators=[InputRequired(), NumberRange(min=0)])
  price = IntegerField("Individual Ticket Price", validators=[InputRequired(), NumberRange(min=0)])
  status = SelectField("Event Status", choices=STATUS_CHOICES, validators=[InputRequired()])
  submit = SubmitField("Update Event")
  
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()], id="comment_input")
  submit = SubmitField('Post', id="comment_submit")

class OrderForm(FlaskForm):
    order_num_tickets = IntegerField("Tickets",validators=[InputRequired()], default=1)
    submit = SubmitField('Order', id="order_submit")
