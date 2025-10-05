from flask import Flask

from app.models.products import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///parking.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)

    return app


