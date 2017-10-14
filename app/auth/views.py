#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/24 17:19
# @Author  : ppy
# @Site    : 
# @File    : views.py
# @Software: PyCharm
import datetime
import itertools
from collections import OrderedDict

from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required, login_user, logout_user, current_user

from .. import login_manager, db
from .models import Role, Menu, User
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


# 注销
@login_required
def logout():
    logout_user()
    res = jsonify(code=1, msg='登出成功')
    res.set_cookie('user_name', expires=0)
    return res


# 修改密码
@login_required
def change_password():
    args = request.get_json()
    params_valid = ("new_password", "old_password")
    error_msg = [x for x in args if x not in params_valid]
    missing_msg = [x for x in params_valid if x not in args]
    if len(error_msg) > 0 or len(args) == 0:
        return jsonify({"error params": error_msg})
    elif len(args) < len(params_valid):
        return jsonify({"missing params": missing_msg})
    old_password = args["old_password"]
    new_password = args["new_password"]
    if current_user is not None and current_user.verify_password(old_password):
        current_user.password = new_password
        current_user.modify_time = datetime.datetime.now()
        db.session.commit()
        return jsonify(code=1, msg="修改密码成功")
    else:
        return jsonify(code=0, msg="修改密码失败，密码错误")


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
        params_valid = ("user_name", "roles", "phone", "email", "name")
        error_msg = [x for x in args if x not in params_valid]
        missing_msg = [x for x in params_valid if x not in args]
        if len(error_msg) > 0 or len(args) == 0:
            return jsonify({"error params": error_msg})
        elif len(args) < len(params_valid):
            return jsonify({"missing params": missing_msg})
        password = '123456'
        user_name, name, roles, phone, email = args['user_name'], args['name'], args['roles'], args['phone'], args['email']
        if not User.query.filter_by(user_name=user_name).first():
            u = User(user_name=user_name, name=name, email=email, phone=phone, password=password)
            # 分配用户组
            if roles:
                u.role = Role.query.filter(Role.id.in_(roles)).all()
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


# 获取用户组下用户
@login_required
@permission_required(Permission.ADMIN)
def role_user():
    args = request.get_json()
    params_valid = ("role_id",)
    page = int(args.pop('page', 1))
    pagesize = int(args.pop('pagesize', 20))
    error_msg = [x for x in args if x not in params_valid]
    missing_msg = [x for x in params_valid if x not in args]
    if len(error_msg) > 0 or len(args) == 0:
        return jsonify({"error params": error_msg})
    elif len(args) < len(params_valid):
        return jsonify({"missing params": missing_msg})
    role_id = args.get('role_id', None)
    role = Role.query.filter(Role.id == role_id).first()
    if role:
        users = role.users.paginate(page=page, per_page=pagesize, error_out=False)
        data = [{'id': x.id, 'user_name': x.user_name, 'name': x.name, 'cellphone': x.phone, 'email': x.email}
                for x in users.items]
        return jsonify(page=page, pages=users.pages, data=data)
    else:
        return jsonify(code=0, msg='用户组不存在')


# 用户组管理类视图
class Roles(MethodView):
    decorators = [permission_required(Permission.ADMIN)]

    # 获取所有用户组
    def get(self):
        page = int(request.args.get('page', 1))
        pagesize = int(request.args.get('pagesize', 20))
        query = Role.query.order_by(Role.id).paginate(page=page, per_page=pagesize, error_out=False)
        data_list = {"page": query.page, "pagesize": query.per_page, "pages": query.pages}
        data_list.update({"items": [{"id": x.id, "name": x.name, 'description': x.description}for x in query.items]})
        return jsonify(data_list)

    # 新增一个用户组
    def post(self):
        args = request.get_json()
        params_valid = ("name", "description", "menus")
        error_msg = [x for x in args if x not in params_valid]
        missing_msg = [x for x in params_valid if x not in args]
        if len(error_msg) > 0 or len(args) == 0:
            return jsonify({"error params": error_msg})
        elif len(args) < len(params_valid):
            return jsonify({"missing params": missing_msg})
        name = args['name']
        description = args['description']
        menu_id = args['menus']
        if not Role.query.filter_by(name=name).first():
            r = Role()
            r.name = name
            r.description = description
            # 添加用户权限菜单
            if len(menu_id) > 0:
                r.menu = Menu.query.filter(Menu.id.in_(menu_id)).all()
                permissions = []
                for menu in r.menu.filter(Menu.parent != 0).all():
                    permissions = list(itertools.chain(permissions, *menu.permissions.with_entities('hex').all()))
                permission = reduce(lambda x, y: x | y, list(permissions))
                r.permission = permission
            db.session.add(r)
            db.session.commit()
            return jsonify(code=1, msg='添加成功！')
        else:
            return jsonify(code=0, msg='用户组已存在！')

    # 更新一个用户组
    def put(self, role_id):
        args = request.get_json()
        params_valid = ("name", "description")
        error_msg = [x for x in args if x not in params_valid]
        missing_msg = [x for x in params_valid if x not in args]
        if len(error_msg) > 0 or len(args) == 0:
            return jsonify({"error params": error_msg})
        elif len(args) < len(params_valid):
            return jsonify({"missing params": missing_msg})
        name = args['name']
        description = args['description']
        role = Role.query.filter_by(id=role_id).first()
        if role:
            if not Role.query.filter_by(name=name).first():
                role.name = name
                role.description = description
                db.session.add(role)
                db.session.commit()
                return jsonify(code=1, msg='修改成功！')
            return jsonify(code=0, msg='用户组已存在！')
        else:
            return jsonify(code=0, msg='该用户组不存在！')

    # 删除一个用户组
    def delete(self, role_id):
        r = Role.query.filter_by(id=role_id).first()
        if r is not None:
            db.session.delete(r)
            db.session.commit()
            return jsonify(code=1, msg='删除成功！')
        else:
            return jsonify(code=0, msg='用户组不存在！')


# 用户组权限管理类
class SetPermission(MethodView):
    decorators = [permission_required(Permission.ADMIN), login_required]

    # 获取组成员资源列表/空白资源列表
    def get(self, role_id):
        # user_id = request.args.get("id", None)
        # 不传入用户组id时 获取空白的权限列表
        if role_id is None:
            menu_list = list()
            menus = Menu.query.filter_by(parent=0).order_by(Menu.sort).all()
            query = Menu.query.filter(Menu.parent != 0).order_by(Menu.parent).order_by(Menu.sort).all()
            items = dict()
            for item in query:
                if item.parent not in items:
                    items[item.parent] = []
                items[item.parent].append(OrderedDict((("id", item.id), ("name", item.name), ("check", False))))
            for item in menus:
                menu_list.append(
                    {
                        "id": item.id,
                        "name": item.name,
                        "items": items[item.id],
                        "check": False
                    }
                )
            return jsonify(menu_list)
        # 传入用户组id时，获取对应用户组的权限列表
        else:
            role = Role.query.get(int(role_id))
            if role is None:
                return jsonify(code=0, msg='该用户组不存在')
            resource_list = [x.id for x in role.menu.order_by(Menu.id).all()]
            permission_list = list()
            menus = Menu.query.filter_by(parent=0).order_by(Menu.sort).all()
            query = Menu.query.filter(Menu.parent != 0).order_by(Menu.parent).order_by(Menu.sort).all()
            items = dict()
            for item in query:
                if item.parent not in items:
                    items[item.parent] = []
                items[item.parent].append(OrderedDict((("id", item.id),
                                                       ("name", item.name),
                                                       ("check", item.id in resource_list))))
            for item in menus:
                permission_list.append(
                    {
                        "id": item.id,
                        "name": item.name,
                        "items": items[item.id],
                        "check":  item.id in resource_list
                    }
                )
            return jsonify(permission_list)

    # 更新用户组权限
    def put(self, role_id):
        role = Role.query.get(int(role_id))
        args = request.get_json()
        params_valid = ("menus",)
        error_msg = [x for x in args if x not in params_valid]
        missing_msg = [x for x in params_valid if x not in args]
        if len(error_msg) > 0 or len(args) == 0:
            return jsonify({"error params": error_msg})
        elif len(args) < len(params_valid):
            return jsonify({"missing params": missing_msg})
        menu_id = args["menus"]
        menus = Menu.query.filter(Menu.id.in_(menu_id)).all()
        if role is not None:
            role.menu = menus
            permissions = []
            for menu in role.menu.filter(Menu.parent != 0).all():
                permissions = list(itertools.chain(permissions, *menu.permissions.with_entities('hex').all()))
            permission = reduce(lambda x, y: x | y, list(permissions))
            role.permission = permission
            db.session.add(role)
            db.session.commit()
            return jsonify(code=1, msg='权限设置成功！')
        else:
            return jsonify(code=0, msg='用户组不存在！')
