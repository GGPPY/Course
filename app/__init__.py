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
from flask_mail import Mail

from config import config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(config.get(config_name))
    config.get(config_name).init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.auth import auth
    app.register_blueprint(auth, url_prefix='/api/auth')

    from app.course import course
    app.register_blueprint(course, url_prefix='/api/course')

    from app.main import main
    app.register_blueprint(main, url_prefix='/api')
    from app.main import media
    app.register_blueprint(media)
    return app
