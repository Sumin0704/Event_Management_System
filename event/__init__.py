from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
UPLOAD_FOLDER = "/static/img"

def create_app():
    app = Flask(__name__)
    
    bootstrap = Bootstrap(app)

    # Configue and initialise DB
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sport.sqlite"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    db.init_app(app)

    app.secret_key = 'junk'

    from . import views
    app.register_blueprint(views.mainbp)

    from . import events
    app.register_blueprint(events.mainbp)

    return app

