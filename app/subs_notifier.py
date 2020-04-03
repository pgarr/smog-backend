# -*- encoding: utf-8 -*-

from app.models import Subscription, SubscriptionHour


def get_hour_subs(hour):
    # funkcja filtrująca subskrypcje na daną godzinę
    return Subscription.query.filter(Subscription.hours.any(SubscriptionHour.hour == hour)).all()
