#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/24 9:56
# @Author  : ppy
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint
from . import views

auth = Blueprint('auth', __name__, url_prefix='/auth')

auth.add_url_rule('/login', view_func=views.login, methods=['POST'])
auth.add_url_rule('/test', view_func=views.test_api, methods=['GET'])

user_view = views.Users.as_view('users')
# 查看用户列表，添加用户
auth.add_url_rule('/users', view_func=user_view, methods=['GET', 'POST'])
# 删除用户，重置密码
auth.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['PUT', 'DELETE'])
