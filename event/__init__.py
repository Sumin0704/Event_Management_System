from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    
    bootstrap = Bootstrap(app)
    app.secret_key = 'junk'

    from . import views
    app.register_blueprint(views.mainbp)

    from . import sports
    app.register_blueprint(sports.mainbp)

    return app

