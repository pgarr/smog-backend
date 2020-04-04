from threading import Thread
from flask import current_app, render_template
from flask_mail import Message


def send_async_email(fl_app, msg):
    with fl_app.app_context():
        from app import mail
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body, attachments=None):
    """attachment - (filename, content_type, data)"""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)

    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()


def send_subscription_email(subscription, data):
    token = subscription.get_change_subscription_token()
    send_email('[Smog-api] Stan twojego powietrza',  # TODO: nazwa aplikacji
               sender=current_app.config['ADMINS'][0],
               recipients=[subscription.email],
               text_body=render_template('email/notification.txt', data=data, front_url=current_app.config['FRONT_URL'],
                                         token=token),  # TODO: templates
               html_body=render_template('email/notification.html', data=data,
                                         front_url=current_app.config['FRONT_URL'], token=token))
