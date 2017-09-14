# coding=utf-8
import datetime

from flask_login import current_user


from .. import db


class CourseType(db.Model):
    __tablename__ = 'course_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    create_user = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    update_user = db.Column(db.String)
    update_time = db.Column(db.DateTime)

    @staticmethod
    def before_insert_func(mapper, connection, target):
        target.create_user = current_user.name
        target.create_time = datetime.datetime.now()

    @staticmethod
    def before_update_func(mapper, connection, target):
        target.update_user = current_user.name
        target.update_time = datetime.datetime.now()

db.event.listen(CourseType, 'before_insert', CourseType.before_insert_func)
db.event.listen(CourseType, 'before_update', CourseType.before_update_func)


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('course_type.id'), nullable=False)
    name = db.Column(db.String)
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    image_path = db.Column(db.String)
    course_url = db.Column(db.String)
    period = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    create_user = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    update_user = db.Column(db.String)
    update_time = db.Column(db.DateTime)

    @staticmethod
    def before_insert_func(mapper, connection, target):
        Course.query.filter(Course.type_id == target.type_id).update({Course.active: False})
        target.create_user = current_user.name
        target.create_time = datetime.datetime.now()

    @staticmethod
    def before_update_func(mapper, connection, target):
        target.update_user = current_user.name
        target.update_time = datetime.datetime.now()

    @staticmethod
    def on_active_change(target, value, oldvalue, initiator):
        if oldvalue is not True:
            Course.query.filter(Course.active.is_(True), Course.type_id == target.type_id).update(
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
    name = db.Column(db.String)
    phone = db.Column(db.String)
    wx = db.Column(db.String)
    ws_name = db.Column(db.String)
    qq = db.Column(db.String)
    area = db.Column(db.String)
    basis = db.Column(db.Boolean)
    size = db.Column(db.String)
    id_card_image = db.Column(db.String)
    pay_image = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    update_user = db.Column(db.String)

    @staticmethod
    def before_insert_func(mapper, connection, target):
        target.create_time = datetime.datetime.now()

    @staticmethod
    def before_update_func(mapper, connection, target):
        target.update_user = current_user.name
        target.update_time = datetime.datetime.now()

db.event.listen(Student, 'before_insert', Student.before_insert_func)
db.event.listen(Student, 'before_update', Student.before_update_func)









