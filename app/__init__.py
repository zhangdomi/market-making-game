from flask import Flask
from .routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # Register the blueprint
    app.register_blueprint(api)

    return app
