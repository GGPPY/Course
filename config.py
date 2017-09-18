#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/24 10:37
# @Author  : ppy
# @Site    : 
# @File    : config.py
# @Software: PyCharm
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or ''
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@127.0.0.1:5432/postgres"
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    CARD_IMAGE_PATH = 'media/card_image'
    PAY_IMAGE_PATH = 'media/pay_image'
    if not os.path.exists(os.path.join(BASEDIR, CARD_IMAGE_PATH)):
        os.makedirs(os.path.join(BASEDIR, CARD_IMAGE_PATH))
    if not os.path.exists(os.path.join(BASEDIR, PAY_IMAGE_PATH)):
        os.makedirs(os.path.join(BASEDIR, PAY_IMAGE_PATH))

    @staticmethod
    def init_app(app):
        pass


class Local(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@127.0.0.1:5432/postgres"

config = {
    "local": Local
}

del os
