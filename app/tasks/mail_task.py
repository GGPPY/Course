# coding=utf-8
import os

from .. import mail, create_app


def send_mail(msg):
    app = create_app(os.getenv('FLASK_CONFIG') or 'local')
    with app.app_context():
        mail.send(msg)
