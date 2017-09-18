# coding=utf-8
import datetime
import random
import os

from flask import current_app, request, send_from_directory, jsonify, url_for, send_from_directory
from werkzeug.utils import secure_filename

from .models import Student, Course, CourseType

ALLOWED_EXTENSIONS = set([u'png', u'jpg', u'jpeg', u'gif'])


def allowed_file(filename):
    return '.' in filename and str(filename.rsplit('.', 1)[1]).lower() in ALLOWED_EXTENSIONS


def post_student():
    if 'multipart/form-data' not in request.content_type:
        return jsonify(code=0, msg='请使用multipart/form-data类型上传表单')

    card_image_front = request.files['card_image_front']
    card_image_back = request.files['card_image_back']
    pay_image = request.files['pay_image']
    card_image_front = image_save("card_image_front", card_image_front)
    card_image_back = image_save("card_image_back", card_image_back)
    pay_image = image_save("pay_image", pay_image)
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

