#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/24 16:13
# @Author  : ppy
# @Site    : 
# @File    : manage.py
# @Software: PyCharm
import os

from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'local')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server(use_reloader=True, host='127.0.0.1', port=5000))

if __name__ == "__main__":
    manager.run()
