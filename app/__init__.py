from flask import Flask

from app.models.products import db
from app.routes.products import product_bp


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
    app.register_blueprint(product_bp)

    with app.app_context():
        db.drop_all()
        db.create_all()

    return app


