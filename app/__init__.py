# app/__init__.py
from flask import Flask
from .config import Config
from .routes import api
import os

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure folders exist at boot, too (defense in depth)
    os.makedirs(app.config["UPLOAD_DIR"], exist_ok=True)
    os.makedirs(app.config["PROCESSED_DIR"], exist_ok=True)

    app.register_blueprint(api, url_prefix="/api")
    return app