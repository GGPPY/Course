#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/24 10:29
# @Author  : ppy
# @Site    : 
# @File    : models.py
# @Software: PyCharm


from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import func
from .. import db, login_manager


login_manager.anonymous_user = AnonymousUserMixin


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

roles_menus = db.Table('roles_menus',
                       db.Column('menu_id', db.Integer, db.ForeignKey('menu.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                       )

menus_permissions = db.Table('menus_permissions',
                             db.Column('menu_id', db.Integer, db.ForeignKey('menu.id')),
                             db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
                             )


class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    name = db.Column(db.String)
    password_hash = db.Column(db.String(128))
    last_login = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime, server_default=func.now())
    create_user = db.Column(db.Integer)
    modify_time = db.Column(db.DateTime)

    role = db.relationship('Role',
                           secondary=roles_users,
                           backref=db.backref('User', lazy='dynamic'),
                           lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password_text):
        self.password_hash = generate_password_hash(password_text, method='pbkdf2:sha1', salt_length=8)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permission):
        roles = self.role
        if roles:
            permissions = reduce(lambda x, y: x | y, [role.permission for role in roles])
            return permissions & permission == permission
        return False


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permission = db.Column(db.Integer)
    menu = db.relationship(
        'Menu',
        secondary=roles_menus,
        backref=db.backref("role", lazy='dynamic'),
        lazy='dynamic'
    )


class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    # 菜单父级id
    parent = db.Column(db.Integer)
    # 菜单名
    name = db.Column(db.String(250))
    # 排序字段
    sort = db.Column(db.Integer)
    # 前端路由
    route = db.Column(db.String(250))

    permissions = db.relationship(
        'Permission',
        secondary=menus_permissions,
        backref=db.backref("permission", lazy='dynamic'),
        lazy='dynamic'
    )


class Permission(db.Model):
    __table_name__ = 'permission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    action = db.Column(db.String(250))
    hex = db.Column(db.Integer)
