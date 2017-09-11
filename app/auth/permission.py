#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/24 10:29
# @Author  : ppy
# @Site    : 
# @File    : permission.py
# @Software: PyCharm
from functools import wraps
from flask import jsonify, abort
from flask_login import current_user


class Permission(object):
    USER_MANAGE = 0x01
    CHANGE_PWD = 0X02
    TEST = 0x04
    ADMIN = 0xff


def permission_required(*permissions):
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            for permission in permissions:
                if current_user.can(permission):
                    return f(*args, **kwargs)
            return abort(403)

        return decorated_func

    return decorator

