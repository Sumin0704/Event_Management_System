from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = 'junk'

    from . import views
    app.register_blueprint(views.mainbp)
    return app

