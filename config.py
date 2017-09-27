#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/24 10:37
# @Author  : ppy
# @Site    : 
# @File    : config.py
# @Software: PyCharm
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'let us go sky'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@127.0.0.1:5432/postgres"
    CELERY_ENABLE_UTC = False
    CELERY_BROKER_URL = 'redis://:linezone@localhost:6379/0',
    CELERY_RESULT_BACKEND = 'redis://:linezone@localhost:6379/1'
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'xudagui@linezonedata.com'
    MAIL_PASSWORD = 'Xx123.'
    MAIL_DEFAULT_SENDER = 'xudagui@linezonedata.com'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    CARD_IMAGE_PATH = 'media/card_image'
    PAY_IMAGE_PATH = 'media/pay_image'
    SUBJECT_IMAGE_PATH = 'media/subject_image'
    for path in (CARD_IMAGE_PATH, PAY_IMAGE_PATH, SUBJECT_IMAGE_PATH):
        if not os.path.exists(os.path.join(BASEDIR, path)):
            os.makedirs(os.path.join(BASEDIR, path))

    @staticmethod
    def init_app(app):
        pass


class Local(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@127.0.0.1:5432/postgres"

config = {
    "local": Local
}

del os
