# -*- encoding: utf-8 -*-
import datetime
import logging

from app.email import send_subscription_email
from app.gios_api import GiosService
from app.models import Subscription, SubscriptionHour

logger = logging.getLogger('notifier')
logger.setLevel(logging.INFO)


def get_hour_subs(hour):
    # funkcja filtrująca subskrypcje na daną godzinę
    logger.info('Get hour %d subscriptions' % hour)
    return Subscription.query.filter(Subscription.hours.any(SubscriptionHour.hour == hour)).all()


def send_notifications(subscriptions):
    for sub in subscriptions:
        try:
            data = GiosService.get_nearest_station_data(sub.lat, sub.lon)
            send_subscription_email(sub, data)
        except Exception as e:
            logger.error('notification failed %s' % sub.email)
            logger.exception(e)
        else:
            logger.info('notify sent %s' % sub.email)


def send_actual_notifications():
    now = datetime.datetime.now()
    logger.info(now.hour)
    subs = get_hour_subs(now.hour)
    send_notifications(subs)
