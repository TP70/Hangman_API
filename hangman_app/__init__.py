from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()


def create_app(config_object):
    """
    Create and configure the Flask app.

    :param config_object: Configuration object for the app.
    :return: Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    mongo.init_app(app)
    from hangman_app.controllers.hangman_controller import api
    app.register_blueprint(api.blueprint)

    return app
