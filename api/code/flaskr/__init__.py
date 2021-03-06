"""This module contains all the code that is used to make this api work."""

from flask import Flask
from flasgger import Swagger
import os

def create_app():
    """ Creates a flask app using the factory pattern. This way, the app can be instantiated with different servers (dev/prod).

    :returns: a flask application
    :rtype: flask.app
    """

    app = Flask(__name__)
    Swagger(app, template_file="swagger.yaml")

    # set configs for db
    db_username = os.getenv('DB_USERNAME')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    app.config['MONGO_URI'] = f'mongodb://{db_username}:{db_password}@mongodb:27017/{db_name}'
    # init extensions
    from flaskr.db import mongo
    mongo.init_app(app)

    # register blueprint(s)
    from flaskr.routes import api_bp
    app.register_blueprint(api_bp)

    return app
