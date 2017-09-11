#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/24 10:37
# @Author  : ppy
# @Site    : 
# @File    : config.py
# @Software: PyCharm
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'wu ya zuo fei ji'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@127.0.0.1:5432/postgres"

    @staticmethod
    def init_app(app):
        pass


class Local(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@127.0.0.1:5432/postgres"

config = {
    "local": Local
}

del os
