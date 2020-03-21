from time import time

import jwt
from flask import current_app

from app import db


class Subscription(db.Model):
    __tablename__ = 'subscription'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    hours = db.relationship('SubscriptionHour', cascade="all, delete-orphan", backref="subscription")

    def add_hour(self, hour):
        if not self.hours:
            self.hours = []
        self.hours.append(SubscriptionHour(hour=hour))

    def get_change_subscription_token(self, expires_in=600):  # TODO: dostosować czas
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def __repr__(self):
        return "Subscription[mail: %s, lat: %d, lon: %d, hours: %s" % (self.email, self.lat, self.lon, self.hours)


class SubscriptionHour(db.Model):
    __tablename__ = 'subscription_hour'

    id = db.Column(db.Integer, primary_key=True)
    hour = db.Column(db.Integer, nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'))

    # nie działa w sql lite
    db.Index('idx_hour_subs_id', 'hour', 'subscription_id', unique=True)

    def __repr__(self):
        return "Hour: %d" % self.hour
