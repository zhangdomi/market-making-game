from flask import Flask


def create_app():
    app = Flask(__name__)
    # app.config.from_object('config')
    
    from .routes import app as routes
    # Register the blueprint
    app.register_blueprint(routes)

    return app
