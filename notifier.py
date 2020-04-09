# -*- encoding: utf-8 -*-
import datetime
import logging
import time

import schedule
from flask import render_template

from app import create_app
from app.email import send_email
from app.gios_api import GiosService
from app.models import Subscription, SubscriptionHour

logger = logging.getLogger('notifier')
logger.setLevel(logging.INFO)


def get_hour_subs(hour):
    # funkcja filtrująca subskrypcje na daną godzinę
    logger.info('Get hour %d subscriptions' % hour)
    return Subscription.query.filter(Subscription.hours.any(SubscriptionHour.hour == hour)).all()


def send_notifications(subscriptions):
    logger.info('%d notifications' % len(subscriptions))
    for sub in subscriptions:
        try:
            data = GiosService.get_nearest_station_data(sub.lat, sub.lon)
            send_subscription_email(sub, data)
        except Exception as e:
            logger.error('notification failed %s' % sub.email)
            logger.exception(e)
        else:
            logger.info('notify sent %s' % sub.email)


def send_subscription_email(subscription, data):
    token = subscription.get_change_subscription_token()
    send_email('[Smog-api] Stan twojego powietrza',  # TODO: nazwa aplikacji
               sender=app.config['ADMINS'][0],
               recipients=[subscription.email],
               text_body=render_template('email/notification.txt', data=data, front_url=app.config['FRONT_URL'],
                                         token=token),  # TODO: templates
               html_body=render_template('email/notification.html', data=data,
                                         front_url=app.config['FRONT_URL'], token=token))


def send_actual_notifications():
    try:
        now = datetime.datetime.now()
        logger.info(now.hour)
        subs = get_hour_subs(now.hour)
        send_notifications(subs)
    except Exception as e:
        logger.error('Notifier error')
        logger.exception(e)


class Notifier:
    def __init__(self, interval=1):
        self.cease_run = False
        self.interval = interval
        schedule.every().hour.at(":00").do(send_actual_notifications)

    def start(self):
        logger.info('Notification scheduler started')
        while not self.cease_run:
            logger.debug('1')
            schedule.run_pending()
            time.sleep(self.interval)
        logger.info('Notification scheduler stopped')

    def stop(self):  # TODO: KeyboardInterrupt
        self.cease_run = True
        logger.info('Notification scheduler stopped')


if __name__ == "__main__":
    app = create_app()
    app.app_context().push()

    notifier = Notifier()
    notifier.start()
