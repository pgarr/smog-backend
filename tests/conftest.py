import pytest

from app import create_app, db
from tests.utils import TestConfig


@pytest.fixture(scope='module')
def test_client():
    # set up
    flask_app = create_app(TestConfig)

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    # tear down
    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # set up
    db.create_all()

    yield db

    # tear down
    db.session.remove()
    db.drop_all()
