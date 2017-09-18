#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/24 9:54
# @Author  : ppy
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


from config import config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(config.get(config_name))
    config.get(config_name).init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    from app.auth import auth
    app.register_blueprint(auth)
    from app.course import course
    app.register_blueprint(course)
    from app.main import main
    app.register_blueprint(main)
    return app
