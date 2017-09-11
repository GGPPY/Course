#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/24 17:19
# @Author  : ppy
# @Site    : 
# @File    : views.py
# @Software: PyCharm
import datetime

from .models import User
from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required, login_user, logout_user

from .. import login_manager, db
from .models import Role
from .permission import Permission, permission_required


# 加载用户
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 未登录状态处理函数
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(code=-1, msg='当前为未登陆状态')


# 登陆
def login():
    """
    :Methods POST
    :param
        user_name:     用户名
        password:   密码
    :return:

    """
    args = request.get_json()
    params_valid = ("user_name", "password")
    error_msg = [x for x in args if x not in params_valid]
    missing_msg = [x for x in params_valid if x not in args]
    if len(error_msg) > 0 or len(args) == 0:
        return jsonify({"error params": error_msg})
    elif len(args) < len(params_valid):
        return jsonify({"missing params": missing_msg})
    user_name = args["user_name"]
    password = args["password"]
    user = User.query.filter_by(user_name=user_name).first()
    if user is not None and user.verify_password(password):
        login_user(user, remember=True)
        db.session.commit()
        res = jsonify(code=1, msg="登陆成功", user_name=unicode(user.name).encode('utf-8'))
        res.set_cookie('user_name', user.name, expires=datetime.datetime.utcnow() + datetime.timedelta(days=7))
        return res
    else:
        return jsonify({"code": 2, "msg": "用户名或密码错误"})


@permission_required(Permission.TEST)
def test_api():
    return jsonify('hello world')


# 用户管理类视图
class Users(MethodView):
    decorators = [permission_required(Permission.ADMIN)]

    # 获取所有用户
    @staticmethod
    def get():
        page = int(request.args.get('page', 1))
        pagesize = int(request.args.get('pagesize', 20))
        query = User.query.order_by(User.id).paginate(page=page, per_page=pagesize, error_out=False)
        data_list = {"page": query.page, "pagesize": query.per_page, "pages": query.pages}
        data_list.update({"items": [{"id": x.id,
                                     "name": x.name}for x in query.items]})
        return jsonify(data_list)

    # 新增用户
    @staticmethod
    def post():
        args = request.get_json()
        params_valid = ("name", "roles", "phone", "email")
        error_msg = [x for x in args if x not in params_valid]
        missing_msg = [x for x in params_valid if x not in args]
        if len(error_msg) > 0 or len(args) == 0:
            return jsonify({"error params": error_msg})
        elif len(args) < len(params_valid):
            return jsonify({"missing params": missing_msg})
        password = '123456'
        name = args['name']
        roles = args['roles']
        phone = args['phone']
        email = args['email']
        if not User.query.filter_by(name=name).first():
            u = User()
            u.password = password
            u.name = name
            u.cellphone = phone
            u.email = email
            # 分配用户组
            if roles:
                u.roles = Role.query.filter(Role.id.in_(roles)).all()
            db.session.add(u)
            db.session.commit()
            return jsonify(code=1, msg='添加成功！')
        else:
            return jsonify(code=0, msg='用户已存在！')

    # 删除用户
    def delete(self, user_id):
        u = User.query.filter_by(id=user_id).first()
        if u is not None:
            db.session.delete(u)
            db.session.commit()
            return jsonify(code=1, msg='删除成功！')
        else:
            return jsonify(code=0, msg='用户不存在！')

    # 密码重置
    def put(self, user_id):
        u = User.query.filter_by(id=user_id).first()
        if u is not None:
            u.password = '123456'
            db.session.add(u)
            db.session.commit()
            return jsonify(code=1, msg='密码重置成功！')
        else:
            return jsonify(code=0, msg='用户不存在！')