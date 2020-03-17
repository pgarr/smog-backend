from unittest import TestCase

from app.models import Subscription, SubscriptionHours


class TestWaitingRecipe(TestCase):
    def test_add_hour_when_dont_exist(self):
        subscription_model = Subscription()
        subscription_model.add_hour(12)

        self.assertEqual(len(subscription_model.hours), 1)

    def test_add_hour_when_exists(self):
        subscription_model = Subscription(hours=[SubscriptionHours(hour=12), SubscriptionHours(hour=14)])
        subscription_model.add_hour(20)

        self.assertEqual(len(subscription_model.hours), 3)

    def test_add_hour_multiple_times(self):
        subscription_model = Subscription(hours=[SubscriptionHours(hour=12)])
        subscription_model.add_hour(14)
        subscription_model.add_hour(20)

        self.assertEqual(len(subscription_model.hours), 3)
