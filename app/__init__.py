# app/__init__.py
from flask import Flask
from config import Config
from flask_cors import CORS


def create_app():
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
    app.config.from_object(Config)

    CORS(app)


    from .routes import setup_routes
    setup_routes(app)

    return app