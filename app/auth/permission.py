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
    CHANGE_PWD = 0X02
    COURSE_MANAGE = 0X04
    STUDENT_MANAGE = 0x08
    ADMIN = 0x10
    SUBJECT_MANGE = 0x20


def permission_required(*permissions):
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            for permission in permissions:
                if not current_user.can(permission):
                    return abort(403)
            return f(*args, **kwargs)

        return decorated_func

    return decorator

