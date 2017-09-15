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
    card_image_front = request.files['card_image']
    basedir = current_app.config['BASEDIR']
    card_image_path = current_app.config['CARD_IMAGE_PATH']
    if card_image_front:
        now_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        random_num = random.randint(0, 100)
        card_image_name = secure_filename(u'front_' + str(now_time) + str(random_num) + '.' +
                                          card_image_front.filename.rsplit('.', 1)[1])
        image_path = os.path.join(card_image_path, card_image_name)
        card_image_front.save(os.path.join(basedir, image_path))
    return jsonify({"url_path": image_path})

