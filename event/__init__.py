from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
UPLOAD_FOLDER = "/static/img"
app = Flask(__name__)

def create_app():
    

    # access to authentication
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    bootstrap = Bootstrap5(app)

    # Configue and initialise DB
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sport.sqlite"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    db.init_app(app)

    app.secret_key = 'junk'

    from . import views
    app.register_blueprint(views.mainbp)

    from . import events
    app.register_blueprint(events.mainbp)

    from . import auth
    app.register_blueprint(auth.mainbp)

    from . import order_route
    app.register_blueprint(order_route.mainbp)

    return app

@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    return render_template("404.html")
