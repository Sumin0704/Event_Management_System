from flask import Blueprint, render_template, session, request, redirect, url_for
from .models import Sport, Comment
from .forms import CommentForm

mainbp = Blueprint("sport", __name__, url_prefix="/sports")

@mainbp.route("/<id>")
def show(id):
    sport = get_sport()
    # brazil = get_destination()
    commentForm = CommentForm()
    return render_template(
        "detail.html", sport=sport, form=commentForm
    )

def get_sport():
    tennis = Sport("QLD Open 2022 Tennis", "hello.jpg", " Sat, 22 Oct", "5:00 – 11:30 pm", "Open(8tickets left)", "13.50(Aud)", "Kedron-Wavell Services Club 21 Kittyhawk Dr, Chermside QLD", "3.8/5.0",
    "Festival will held")
    comment1 = Comment("Sumin", "I like to go there agian", "12:00:00")
    comment2 = Comment("Jenny", "It's dangerous", "12:05:10")
    tennis.add_comment(comment1)
    tennis.add_comment(comment2)
    return tennis

@mainbp.route("/<id>/comment", methods=["POST"])
def comment(id):
    # here the form is created  form = CommentForm()
    commentForm = CommentForm()
    if commentForm.validate_on_submit():  # this is true only in case of POST method
        print("The following comment has been posted:")
    # notice the signature of url_for
    return redirect(url_for("sport.show", id=1))