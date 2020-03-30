import pytest

from app import create_app, db
from app.models import Subscription, SubscriptionHour
from tests.utils import TestConfig


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""
    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture
def test_client():
    # set up
    flask_app = create_app(TestConfig)

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    # tear down
    ctx.pop()


@pytest.fixture
def database():
    # set up
    db.create_all()

    yield db

    # tear down
    db.session.remove()
    db.drop_all()


@pytest.fixture
def make_subscription(database):
    def _make_sub(email, lat, lon, hours):
        sub = Subscription(email=email, lat=lat, lon=lon)
        sub.hours = [SubscriptionHour(hour=h) for h in hours]

        database.session.add(sub)
        database.session.commit()

        return sub

    return _make_sub
