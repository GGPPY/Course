# coding=utf-8
import datetime

from flask_login import current_user

from .. import db


class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    subject_image = db.Column(db.String)
    subject_url = db.Column(db.String)
    course = db.relationship("Course", back_populates="subject")
    create_user = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    update_user = db.Column(db.String)
    update_time = db.Column(db.DateTime)

    def __init__(self, kwargs):
        valid_keys = ('name', 'subject_image', 'subject_url')
        for key, value in kwargs.iteritems():
            if key in valid_keys:
                self.__setattr__(key, value)

    def update(self, kwargs):
        valid_keys = ('name', 'subject_image', 'subject_url')
        for key, value in kwargs.iteritems():
            if key in valid_keys:
                self.__setattr__(key, value)

    @staticmethod
    def before_insert_func(mapper, connection, target):
        # target.create_user = current_user.name
        target.create_time = datetime.datetime.now()

    @staticmethod
    def before_update_func(mapper, connection, target):
        # target.update_user = current_user.name
        target.update_time = datetime.datetime.now()

db.event.listen(Subject, 'before_insert', Subject.before_insert_func)
db.event.listen(Subject, 'before_update', Subject.before_update_func)


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship("Subject", back_populates="course")
    name = db.Column(db.String)
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    period = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    create_user = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    update_user = db.Column(db.String)
    update_time = db.Column(db.DateTime)

    students = db.relationship("Student", back_populates='course')

    def __init__(self, kwargs):
        valid_keys = ('name', 'subject_id', 'start_time', 'end_time', 'period')
        for key, value in kwargs.iteritems():
            if key in valid_keys:
                self.__setattr__(key, value)

    def update(self, kwargs):
        valid_keys = ('name', 'subject_id', 'start_time', 'end_time', 'period')
        for key, value in kwargs.iteritems():
            if key in valid_keys:
                self.__setattr__(key, value)

    @staticmethod
    def before_insert_func(mapper, connection, target):
        Course.query.filter(Course.subject_id == target.subject_id).update({Course.active: False})
        # target.create_user = current_user.name
        target.create_time = datetime.datetime.now()

    @staticmethod
    def before_update_func(mapper, connection, target):
        # target.update_user = current_user.name
        target.update_time = datetime.datetime.now()

    @staticmethod
    def on_active_change(target, value, oldvalue, initiator):
        if oldvalue is not True:
            Course.query.filter(Course.active.is_(True), Course.subject_id == target.subject_id).update(
                {Course.active: False})
        else:
            pass
        db.session.commit()

db.event.listen(Course, 'before_insert', Course.before_insert_func)
db.event.listen(Course, 'before_update', Course.before_update_func)
db.event.listen(Course.active, 'set', Course.on_active_change)


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship("Course", back_populates="students")
    name = db.Column(db.String)
    phone = db.Column(db.String)
    wx = db.Column(db.String)
    wx_name = db.Column(db.String)
    qq = db.Column(db.String)
    area = db.Column(db.String)
    base = db.Column(db.Boolean)
    size = db.Column(db.String)
    card_image_front = db.Column(db.String)
    card_image_back = db.Column(db.String)
    pay_image = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    update_user = db.Column(db.String)

    def __init__(self, kwargs):
        valid_keys = ('card_image_front', 'card_image_back', 'pay_image', 'course_id', 'name', 'phone', 'wx', 'wx_name',
                      'qq', 'area', 'base', 'size')

        for key, value in kwargs.iteritems():
            if key in valid_keys:
                self.__setattr__(key, value)

    def update(self, person_info):
        self.__init__(person_info)

    @staticmethod
    def before_insert_func(mapper, connection, target):
        target.create_time = datetime.datetime.now()

    @staticmethod
    def before_update_func(mapper, connection, target):
        if not current_user.is_anonymous:
            target.update_user = current_user.name
        target.update_time = datetime.datetime.now()

db.event.listen(Student, 'before_insert', Student.before_insert_func)
db.event.listen(Student, 'before_update', Student.before_update_func)
