#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/24 9:56
# @Author  : ppy
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint
from . import views

auth = Blueprint('auth', __name__)

# 登录
auth.add_url_rule('/login', view_func=views.login, methods=['POST'])
# 注销
auth.add_url_rule('/logout', view_func=views.logout, methods=['GET'])

# 修改密码
auth.add_url_rule('/password', view_func=views.change_password, methods=['POST'])

user_view = views.Users.as_view('users')
# 查看用户列表，添加用户
auth.add_url_rule('/users', view_func=user_view, methods=['GET', 'POST'])
# 删除用户，重置密码
auth.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['PUT', 'DELETE'])

role_view = views.Roles.as_view('role')
# 查看所有用户组，添加组
auth.add_url_rule('/roles', view_func=role_view, methods=['GET', 'POST'])
# 删除，更新用户组
auth.add_url_rule('/roles/<int:role_id>', view_func=role_view, methods=['PUT', 'DELETE'])

# 查看用户组下用户
auth.add_url_rule('/roles/users', view_func=views.role_user, methods=['POST'])

role_permission = views.SetPermission.as_view('permission')
# 查看用户组权限
auth.add_url_rule('/roles/permission/', defaults={"role_id": None}, view_func=role_permission, methods=['GET', ])
# 设置用户组权限
auth.add_url_rule('/roles/permission/<int:role_id>', view_func=role_permission, methods=['PUT', 'GET'])
