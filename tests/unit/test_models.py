from app.models import Subscription, SubscriptionHour


def test_add_hour_when_dont_exist():
    subscription_model = Subscription()
    subscription_model.add_hour(12)

    assert len(subscription_model.hours) == 1


def test_add_hour_when_exists():
    subscription_model = Subscription(hours=[SubscriptionHour(hour=12), SubscriptionHour(hour=14)])
    subscription_model.add_hour(20)

    assert len(subscription_model.hours) == 3


def test_add_hour_multiple_times():
    subscription_model = Subscription(hours=[SubscriptionHour(hour=12)])
    subscription_model.add_hour(14)
    subscription_model.add_hour(20)

    assert len(subscription_model.hours) == 3


def test_get_int_hours_dont_exist():
    subscription_model = Subscription()
    assert subscription_model.get_int_hours() == []


def test_get_int_hours_empty():
    subscription_model = Subscription(hours=[])
    assert subscription_model.get_int_hours() == []


def test_get_int_hours_one():
    subscription_model = Subscription(hours=[SubscriptionHour(hour=12)])
    assert subscription_model.get_int_hours() == [12]


def test_get_int_hours_many_sorted():
    subscription_model = Subscription(
        hours=[SubscriptionHour(hour=12), SubscriptionHour(hour=14), SubscriptionHour(hour=16)])
    assert subscription_model.get_int_hours() == [12, 14, 16]


def test_get_int_hours_many_unsorted():
    subscription_model = Subscription(
        hours=[SubscriptionHour(hour=14), SubscriptionHour(hour=16), SubscriptionHour(hour=12)])
    assert subscription_model.get_int_hours() == [12, 14, 16]
