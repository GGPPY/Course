# coding=utf-8
import os
import threading

from flask import current_app, jsonify, request, session, send_from_directory
from werkzeug.datastructures import FileStorage
from flask.views import MethodView
from flask_mail import Message

from .. import db
from ..course.models import Student, Course, Subject
from ..course.views import image_save, allowed_file, ALLOWED_EXTENSIONS
from ..tasks.mail_task import send_mail


def media(path):
    basedir = current_app.config['BASEDIR']
    media_path = os.path.join(basedir, 'media')
    return send_from_directory(media_path, path)


# 学员报名视图 增删改查
class StudentView(MethodView):

    @staticmethod
    def get():
        args = request.args
        params_valid = ('phone', 'name', 'course_id')
        missing_msg = [x for x in params_valid if x not in args]
        student_id = args.get('id')
        if len(missing_msg) > 0 and not student_id:
            return jsonify({"code": 0, "msg": "missing params: " + str(missing_msg)})
        phone = args.get('phone')
        name = args.get('name')
        course_id = args.get('course_id')
        rule = [Student.phone == phone, Student.course_id == course_id, Student.name == name]
        if student_id:
            rule = [Student.id == student_id]
        column = list(Student.__table__.c)
        column.extend([Course.start_time, Course.end_time, Subject.name.label('course_name')])
        data = Student.query.with_entities(*column).join(Course, Student.course_id == Course.id)\
            .join(Subject, Course.subject_id == Subject.id)\
            .filter(*rule).first()
        if data:
            session.update({"student_id": data.id})
            return jsonify({"code": 1, "msg": "查询成功", "data": data})
        return jsonify({"code": 0, "msg": "找不到相关学员信息", "data": []})

    @staticmethod
    def post():
        if 'multipart/form-data' not in request.content_type:
            return jsonify(code=0, msg='请使用multipart/form-data类型上传表单')
        params_valid = ('card_image_front', 'card_image_back', 'pay_image', 'course_id', 'name', 'phone', 'wx',
                        'wx_name', 'qq', 'area', 'base', 'size')
        params_null = ('wx_name', 'qq', 'area')
        args = request.files.to_dict()
        args.update(request.form.to_dict())
        error_msg = [x for x in args if x not in params_valid]
        missing_msg = [x for x in params_valid if x not in args and x not in params_null]
        null_msg = [key for key, value in args.iteritems() if not value and key not in params_null]
        if error_msg:
            return jsonify({"code": 0, "msg": "参数错误"})
        if missing_msg:
            return jsonify({"code": 0, "msg": "缺少报名信息"})
        if null_msg:
            return jsonify({"code": 0, "msg": "缺少报名信息"})

        # 图片格式判断&存储
        for image_key in ("card_image_front", "card_image_back", "pay_image"):
            image_file = args.get(image_key)
            if not image_file:
                continue
            if not allowed_file(image_file.filename):
                return jsonify({"code": 0, "msg": "图片格式不正确，仅允许一下格式 " + str(ALLOWED_EXTENSIONS)})
            # 保存文件
            image_path = image_save(image_key, image_file)
            # 参数更新
            args.update({image_key: image_path})

        course = Course.query.filter(Course.id == args.get('course_id', None)).first()
        if not course:
            return jsonify({"code": 0, "msg": "课程不存在"})

        exist_rule = [Student.phone == args.get('phone'), Student.course_id == args.get('course_id'),
                      Student.name == args.get('name')]
        student = Student.query.filter(*exist_rule).first()
        if student:
            return jsonify({"code": 0, "msg": "已报名该课程"})
        student = Student(args)
        db.session.add(student)
        db.session.commit()

        # 邮件发送
        msg = Message(u'{subject}有新学员报名'.format(subject=u'课程A'), recipients=['476991811@qq.com'])
        msg.body = u'{student}报名课程{subject}'.format(student=args.get('name'), subject=u'课程A')
        send_mail_thread = threading.Thread(target=send_mail, args=(msg,))
        send_mail_thread.start()
        return jsonify({"code": 1, "msg": "报名成功"})

    @staticmethod
    def put():
        student_id = session.get('student_id', None)
        if not student_id:
            return jsonify({"code": 0, "msg": "请先查询报名信息"})
        if 'multipart/form-data' not in request.content_type:
            return jsonify(code=0, msg='请使用multipart/form-data类型上传表单')
        params_valid = ('card_image_front', 'card_image_back', 'pay_image', 'course_id', 'name', 'phone', 'wx',
                        'wx_name', 'qq', 'area', 'base', 'size')
        params_null = ('wx_name', 'qq', 'area', 'card_image_front', 'card_image_back', 'pay_image', 'course_id',
                       'name', 'phone', 'wx', 'base', 'size')
        args = request.files.to_dict()
        args.update(request.form.to_dict())
        error_msg = [x for x in args if x not in params_valid]
        missing_msg = [x for x in params_valid if x not in args and x not in params_null]
        null_msg = [key for key, value in args.iteritems() if not value and key not in params_null]
        if error_msg:
            return jsonify({"code": 0, "msg": "参数错误"})
        if null_msg or len(args) < 1:
            return jsonify({"code": 0, "msg": "缺少报名信息"})

        course = Course.query.filter(Course.id == args.get('course_id', None)).first()
        if not course:
            return jsonify({"code": 0, "msg": "课程不存在"})

        student = Student.query.filter(Student.id == student_id).first()
        if not student:
            return jsonify({"code": 0, "msg": "学员不存在"})

        for image_key in ("card_image_front", "card_image_back", "pay_image"):
            image_file = args.get(image_key)
            if not image_file or not isinstance(image_file, FileStorage):
                continue
            if not allowed_file(image_file.filename):
                return jsonify({"code": 0, "msg": "图片格式不正确，仅允许一下格式 " + str(ALLOWED_EXTENSIONS)})
            # 保存文件
            image_path = image_save(image_key, image_file)
            # 参数更新
            args.update({image_key: image_path})

        student.update(args)
        db.session.add(student)
        db.session.commit()
        return jsonify({"code": 1, "msg": "更新成功"})
