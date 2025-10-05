import pytest

from app.models.products import db
from app import create_app


@pytest.fixture(scope="session")
def app():
    import tempfile
    tmp_dir = tempfile.mkdtemp()

    _app = create_app(
        {
            "TESTING": True,
            "INSTANCE_PATH": tmp_dir,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "WTF_CSRF_ENABLED": False
        }
    )

    with _app.app_context():
        db.create_all()

        yield _app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    yield app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()