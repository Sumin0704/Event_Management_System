from flask import Blueprint, render_template, session, request, redirect, url_for

mainbp = Blueprint("main",__name__)

@mainbp.route("/")
def index():
    return render_template('index.html')

@mainbp.route("/login")
def login():
    return render_template('login.html')

@mainbp.route("/handelLoginForm", methods=["POST"])
def handelLoginForm():
    session["email"] = request.values.get("email")
    return redirect(url_for("main.index"))

@mainbp.route("/logout")
def logout():
    session.pop("email")
    return "User logged out"

@mainbp.route("/history")
def history():
    return render_template('history.html')

@mainbp.route("/create")
def create():
    return render_template('create.html')
