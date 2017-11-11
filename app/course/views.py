# coding=utf-8
import datetime
import random
import os

from flask import current_app, request, jsonify
from flask.views import MethodView
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


from .. import db
from .models import Student, Course, Subject

ALLOWED_EXTENSIONS = set([u'png', u'jpg', u'jpeg', u'gif', u'bmp'])


def allowed_file(filename):
    return '.' in filename and str(filename.rsplit('.', 1)[1]).lower() in ALLOWED_EXTENSIONS


# 图片保存函数
def image_save(image_type, image):
    basedir = current_app.config['BASEDIR']
    card_image_path = current_app.config['CARD_IMAGE_PATH']
    pay_image_path = current_app.config['PAY_IMAGE_PATH']
    subject_image_path = current_app.config['SUBJECT_IMAGE_PATH']
    image_types = {
        "subject_image": {
            "prefix": "subject_",
            "path": subject_image_path
        },
        "card_image_front": {
            "prefix": "front_",
            "path": card_image_path
        },
        "card_image_back": {
            "prefix": "back_",
            "path": card_image_path
        },
        "pay_image": {
            "prefix": "pay_",
            "path": pay_image_path
        },
    }
    prefix = image_types.get(image_type).get('prefix')
    path = image_types.get(image_type).get('path')
    now_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    random_num = random.randint(0, 100)
    image_name = secure_filename(prefix + str(now_time) + str(random_num) + '.' + image.filename.rsplit('.', 1)[1])
    image_path = os.path.join(path, image_name)
    image.save(os.path.join(basedir, image_path))
    return '/{path}'.format(path=image_path.replace('\\', '/'))


def course_list():
    pass


def course_apply():
    if 'multipart/form-data' not in request.content_type:
        return jsonify(code=0, msg='请使用multipart/form-data类型上传表单')
    params_valid = ('card_image_front', 'card_image_back', 'pay_image', 'course_id', 'name', 'phone', 'wx', 'wx_name',
                    'qq', 'area', 'base', 'size')
    params_null = ('wx_name', )
    args = request.files.to_dict()
    args.update(request.form.to_dict())
    error_msg = [x for x in args if x not in params_valid]
    missing_msg = [x for x in params_valid if x not in args and x not in params_null]
    null_msg = [key for key, value in args.iteritems() if not value and key not in params_null]
    if len(error_msg) > 0:
        return jsonify({"code": 0, "msg": "error params: " + str(error_msg)})
    if len(args) < len(params_valid) - len(params_null):
        return jsonify({"code": 0, "msg": "missing params: " + str(missing_msg)})
    if len(null_msg) > 0:
        return jsonify({"code": 0, "msg": "params can't be null: " + str(null_msg)})
    card_image_front = args.get('card_image_front')
    card_image_back = args.get('card_image_back')
    pay_image = args.get('pay_image')
    for image_file in (card_image_front, card_image_back, pay_image):
        if not allowed_file(image_file.filename):
            return jsonify({"code": 0, "msg": "only allow image types: " + str(ALLOWED_EXTENSIONS)})
    card_image_front = image_save("card_image_front", card_image_front)
    card_image_back = image_save("card_image_back", card_image_back)
    pay_image = image_save("pay_image", pay_image)
    args.update({"card_image_front": card_image_front, "card_image_back": card_image_back, "pay_image": pay_image})
    s = Student(args)
    db.session.add(s)
    db.session.commit()
    return jsonify({"front": card_image_front, "back": card_image_back, "pay": pay_image})


# 科目视图 增删改查
class SubjectView(MethodView):

    @staticmethod
    def get():
        data = Subject.query.with_entities(*Subject.__table__.c).all()
        return jsonify(data)

    @staticmethod
    def post():
        if 'multipart/form-data' not in request.content_type:
            return jsonify(code=0, msg='请使用multipart/form-data类型上传表单')
        params_valid = ('name', 'subject_image', 'subject_url')
        args = request.files.to_dict()
        args.update(request.form.to_dict())

        error_msg = [x for x in args if x not in params_valid]
        missing_msg = [x for x in params_valid if x not in args]
        null_msg = [key for key, value in args.iteritems() if not value]
        if len(error_msg) > 0:
            return jsonify({"code": 0, "msg": "error params: " + str(error_msg)})
        if len(args) < len(params_valid):
            return jsonify({"code": 0, "msg": "missing params: " + str(missing_msg)})
        if len(null_msg) > 0:
            return jsonify({"code": 0, "msg": "params can't be null: " + str(null_msg)})
        subject_image = args.get('subject_image')
        if not allowed_file(subject_image.filename):
            return jsonify({"code": 0, "msg": "only allow image types: " + str(ALLOWED_EXTENSIONS)})
        subject_image = image_save("subject_image", subject_image)
        args.update({"subject_image": subject_image})
        s = Subject(kwargs=args)
        db.session.add(s)
        db.session.commit()
        return jsonify({"code": 1, "msg": "添加科目成功"})

    @staticmethod
    def put(subject_id):
        if 'multipart/form-data' not in request.content_type:
            return jsonify(code=0, msg='请使用multipart/form-data类型上传表单')
        params_valid = ('name', 'subject_image', 'subject_url')
        args = request.files.to_dict()
        args.update(request.form.to_dict())

        error_msg = [x for x in args if x not in params_valid]
        missing_msg = [x for x in params_valid if x not in args]
        null_msg = [key for key, value in args.iteritems() if not value]
        if len(error_msg) > 0:
            return jsonify({"code": 0, "msg": "error params: " + str(error_msg)})
        if len(args) < len(params_valid):
            return jsonify({"code": 0, "msg": "missing params: " + str(missing_msg)})
        if len(null_msg) > 0:
            return jsonify({"code": 0, "msg": "params can't be null: " + str(null_msg)})
        subject_image = args.get('subject_image')
        if not allowed_file(subject_image.filename):
            return jsonify({"code": 0, "msg": "only allow image types: " + str(ALLOWED_EXTENSIONS)})
        args['subject_image'] = image_save("subject_image", subject_image)
        s = Subject.query.filter(Subject.id == subject_id).first()
        if s:
            s.update(args)
            db.session.add(s)
            db.session.commit()
            return jsonify({"code": 1, "msg": "更新成功"})
        return jsonify({"code": 0, "msg": "科目不存在"})

    @staticmethod
    def delete(subject_id):
        s = Subject.query.filter(Subject.id == subject_id).first()
        if s:
            db.session.delete(s)
            db.session.commit()
            return jsonify({"code": 1, "msg": "删除成功"})
        return jsonify({"code": 0, "msg": "科目不存在"})


# 课程视图 增删改查
class CourseView(MethodView):

    @staticmethod
    def get():
        column = list(Course.__table__.c)
        column.append(Subject.name.label('subject_name'))
        data = Course.query.with_entities(*column).join(Subject, Course.subject_id == Subject.id).all()
        return jsonify(data)

    @staticmethod
    def post():
        args = request.get_json()
        params_valid = ('name', 'subject_id', 'start_time', 'end_time', 'period')
        error_msg = [x for x in args if x not in params_valid]
        missing_msg = [x for x in params_valid if x not in args]
        null_msg = [key for key, value in args.iteritems() if not value]
        if len(error_msg) > 0:
            return jsonify({"code": 0, "msg": "error params: " + str(error_msg)})
        if len(args) < len(params_valid):
            return jsonify({"code": 0, "msg": "missing params: " + str(missing_msg)})
        if len(null_msg) > 0:
            return jsonify({"code": 0, "msg": "params can't be null: " + str(null_msg)})
        course = Course(args)
        db.session.add(course)
        db.session.commit()
        return jsonify({"code": 1, "msg": "课程添加成功"})

    @staticmethod
    def put(course_id):
        args = request.get_json()
        params_valid = ('name', 'subject_id', 'start_time', 'end_time', 'period')
        error_msg = [x for x in args if x not in params_valid]
        missing_msg = [x for x in params_valid if x not in args]
        null_msg = [key for key, value in args.iteritems() if not value]
        if len(error_msg) > 0:
            return jsonify({"code": 0, "msg": "error params: " + str(error_msg)})
        if len(args) < len(params_valid):
            return jsonify({"code": 0, "msg": "missing params: " + str(missing_msg)})
        if len(null_msg) > 0:
            return jsonify({"code": 0, "msg": "params can't be null: " + str(null_msg)})

        error_msg = [x for x in args if x not in params_valid]
        missing_msg = [x for x in params_valid if x not in args]
        null_msg = [key for key, value in args.iteritems() if not value]
        if len(error_msg) > 0:
            return jsonify({"code": 0, "msg": "error params: " + str(error_msg)})
        if len(args) < len(params_valid):
            return jsonify({"code": 0, "msg": "missing params: " + str(missing_msg)})
        if len(null_msg) > 0:
            return jsonify({"code": 0, "msg": "params can't be null: " + str(null_msg)})
        course = Course.query.filter(Course.id == course_id).first()
        if course:
            course.update(args)
            db.session.add(course)
            db.session.commit()
            return jsonify({"code": 1, "msg": "更新成功"})
        return jsonify({"code": 0, "msg": "课程不存在"})

    @staticmethod
    def delete(course_id):
        course = Course.query.filter(Course.id == course_id).first()
        if course:
            if course.active:
                return jsonify({"code": 0, "msg": "无法删除激活状态的课程"})
            if course.students:
                return jsonify({"code": 0, "msg": "无法删除有学员的课程"})
            db.session.delete(course)
            db.session.commit()
            return jsonify({"code": 1, "msg": "删除成功"})
        return jsonify({"code": 0, "msg": "科目不存在"})


# 学员视图 增删改查
class StudentView(MethodView):

    @staticmethod
    def get():
        column = list(Student.__table__.c)
        column.append(Course.name.label('course_name'))
        data = Student.query.with_entities(*column).join(Course, Student.course_id == Course.id).all()
        return jsonify(data)

    @staticmethod
    def post():
        if 'multipart/form-data' not in request.content_type:
            return jsonify(code=0, msg='请使用multipart/form-data类型上传表单')
        params_valid = ('card_image_front', 'card_image_back', 'pay_image', 'course_id', 'name', 'phone', 'wx',
                        'wx_name', 'qq', 'area', 'base', 'size')
        params_null = ('wx_name',)
        args = request.files.to_dict()
        args.update(request.form.to_dict())
        error_msg = [x for x in args if x not in params_valid]
        missing_msg = [x for x in params_valid if x not in args and x not in params_null]
        null_msg = [key for key, value in args.iteritems() if not value and key not in params_null]
        if len(error_msg) > 0:
            return jsonify({"code": 0, "msg": "error params: " + str(error_msg)})
        if len(args) < len(params_valid) - len(params_null):
            return jsonify({"code": 0, "msg": "missing params: " + str(missing_msg)})
        if len(null_msg) > 0:
            return jsonify({"code": 0, "msg": "params can't be null: " + str(null_msg)})

        # 图片格式判断&存储
        for image_key in ("card_image_front", "card_image_back", "pay_image"):
            image_file = args.get(image_key)
            if not image_file:
                continue
            if not allowed_file(image_file.filename):
                return jsonify({"code": 0, "msg": "only allow image types: " + str(ALLOWED_EXTENSIONS)})
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
        return jsonify({"code": 1, "msg": "报名成功"})

    @staticmethod
    def put(student_id):
        if 'multipart/form-data' not in request.content_type:
            return jsonify(code=0, msg='请使用multipart/form-data类型上传表单')
        params_valid = ('card_image_front', 'card_image_back', 'pay_image', 'course_id', 'name', 'phone', 'wx',
                        'wx_name', 'qq', 'area', 'base', 'size')
        params_null = ('wx_name', 'qq', 'area', 'card_image_front', 'card_image_back', 'pay_image', 'course_id',
                       'name', 'phone', 'wx', 'base', 'size')
        args = request.files.to_dict()
        args.update(request.form.to_dict())
        error_msg = [x for x in args if x not in params_valid]
        null_msg = [key for key, value in args.iteritems() if not value and key not in params_null]
        if len(error_msg) > 0:
            return jsonify({"code": 0, "msg": "error params: " + str(error_msg)})
        if null_msg or len(args) < 1:
            return jsonify({"code": 0, "msg": "params can't be null: " + str(null_msg)})

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
                return jsonify({"code": 0, "msg": "only allow image types: " + str(ALLOWED_EXTENSIONS)})
            # 保存文件
            image_path = image_save(image_key, image_file)
            # 参数更新
            args.update({image_key: image_path})

        student.update(args)
        db.session.add(student)
        db.session.commit()
        return jsonify({"code": 1, "msg": "更新成功"})

    @staticmethod
    def delete(student_id):
        student = Student.query.filter(Student.id == student_id).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            return jsonify({"code": 1, "msg": "删除成功"})
        return jsonify({"code": 0, "msg": "学员不存在"})


