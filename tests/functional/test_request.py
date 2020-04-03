from app.models import Subscription


def test_connection(test_client):
    response = test_client.get('/api/')
    assert response.status_code == 200


def test_register(test_client, database):
    email = "sample@test.pl"
    lat = 51.1234
    lon = 21.0101
    hours = [12, 14, 20]

    response = test_client.post('/api/register',
                                json={"email": email, "lat": lat, "lon": lon, "hours": hours})
    assert response.status_code == 200

    subscriptions = Subscription.query.all()
    assert len(subscriptions) == 1

    sub = subscriptions[0]
    assert sub.email == email
    assert sub.lat == lat
    assert sub.lon == lon
    assert sub.get_int_hours() == hours


def test_register_no_data(test_client, database):
    response = test_client.post('/api/register')
    assert response.status_code == 400

    subscriptions = Subscription.query.all()
    assert len(subscriptions) == 0


def test_register_email_occupied(test_client, database, make_subscription):
    email = "sample@test.pl"
    lat = 51.1234
    lon = 21.0101
    hours = [12, 14, 20]

    sub = make_subscription(email, lat, lon, hours)

    response = test_client.post('/api/register',
                                json={"email": email, "lat": lat, "lon": lon, "hours": hours})

    assert response.status_code == 422

    subscriptions = Subscription.query.all()
    assert len(subscriptions) == 1


def test_register_no_email(test_client, database):
    lat = 51.1234
    lon = 21.0101
    hours = [12, 14, 20]

    response = test_client.post('/api/register',
                                json={"lat": lat, "lon": lon, "hours": hours})

    assert response.status_code == 422

    subscriptions = Subscription.query.all()
    assert len(subscriptions) == 0


def test_register_no_lat(test_client, database):
    email = "sample@test.pl"
    lon = 21.0101
    hours = [12, 14, 20]

    response = test_client.post('/api/register',
                                json={"email": email, "lon": lon, "hours": hours})

    assert response.status_code == 422

    subscriptions = Subscription.query.all()
    assert len(subscriptions) == 0


def test_register_no_lon(test_client, database):
    email = "sample@test.pl"
    lat = 51.1234
    hours = [12, 14, 20]

    response = test_client.post('/api/register',
                                json={"email": email, "lat": lat, "hours": hours})

    assert response.status_code == 422

    subscriptions = Subscription.query.all()
    assert len(subscriptions) == 0


def test_register_no_hours(test_client, database):
    email = "sample@test.pl"
    lat = 51.1234
    lon = 21.0101

    response = test_client.post('/api/register',
                                json={"email": email, "lat": lat, "lon": lon})

    assert response.status_code == 422

    subscriptions = Subscription.query.all()
    assert len(subscriptions) == 0
