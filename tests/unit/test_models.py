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


def test_update_hours_less():
    subscription_model = Subscription(
        hours=[SubscriptionHour(hour=12), SubscriptionHour(hour=14), SubscriptionHour(hour=16)])

    subscription_model.update_hours([4, 5])

    assert len(subscription_model.hours) == 2
    assert subscription_model.hours[0].hour == 4
    assert subscription_model.hours[1].hour == 5


def test_update_hours_when_not_exist():
    subscription_model = Subscription()

    subscription_model.update_hours([4, 5])

    assert len(subscription_model.hours) == 2
    assert subscription_model.hours[0].hour == 4
    assert subscription_model.hours[1].hour == 5


def test_update_hours_more():
    subscription_model = Subscription(
        hours=[SubscriptionHour(hour=12), SubscriptionHour(hour=14), SubscriptionHour(hour=16)])

    subscription_model.update_hours([4, 5, 6, 7, 8])

    assert len(subscription_model.hours) == 5
    assert subscription_model.hours[0].hour == 4
    assert subscription_model.hours[1].hour == 5
    assert subscription_model.hours[2].hour == 6
    assert subscription_model.hours[3].hour == 7
    assert subscription_model.hours[4].hour == 8


def test_update_hours_wih_duplicates():
    subscription_model = Subscription(
        hours=[SubscriptionHour(hour=12), SubscriptionHour(hour=14), SubscriptionHour(hour=16)])

    subscription_model.update_hours([4, 5, 6, 7, 8, 4, 5, 6, 7, 8])

    assert len(subscription_model.hours) == 5
    assert subscription_model.hours[0].hour == 4
    assert subscription_model.hours[1].hour == 5
    assert subscription_model.hours[2].hour == 6
    assert subscription_model.hours[3].hour == 7
    assert subscription_model.hours[4].hour == 8
