from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
UPLOAD_FOLDER = "/static/img"

def create_app():
    app = Flask(__name__)

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

    return app

