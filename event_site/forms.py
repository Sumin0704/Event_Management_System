from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo


ALLOWED_FILE = {"PNG", "JPG", "JPEG", "png", "jpg", "jpeg"}

class LoginForm(FlaskForm):
    name = StringField("User Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
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
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")


class EventForm(FlaskForm):
  name = StringField("Event Name", validators=[InputRequired()])
  # adding two validators, one to ensure input is entered and other to check if the
  # description meets the length requirements
  type = StringField("Event Type", validators=[InputRequired()])
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
  price = StringField("Price", validators=[InputRequired()])
  submit = SubmitField("Create")

class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Post')

# need a buy tickets form