# coding=utf-8
import datetime
import random
import os

from flask import current_app, request, send_from_directory, jsonify, url_for, send_from_directory
from werkzeug.utils import secure_filename

from .. import db
from .models import Student, Course, CourseType

ALLOWED_EXTENSIONS = set([u'png', u'jpg', u'jpeg', u'gif', u'bmp'])


def allowed_file(filename):
    return '.' in filename and str(filename.rsplit('.', 1)[1]).lower() in ALLOWED_EXTENSIONS


def post_student():
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
    card_image_front = request.files['card_image_front']
    card_image_back = request.files['card_image_back']
    pay_image = request.files['pay_image']
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


def image_save(image_type, image):
    basedir = current_app.config['BASEDIR']
    card_image_path = current_app.config['CARD_IMAGE_PATH']
    pay_image_path = current_app.config['PAY_IMAGE_PATH']
    image_types = {
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

