# coding=utf-8
import datetime
import random
import os

from flask import current_app, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename

from .models import Student, Course, CourseType

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and str(filename.rsplit('.', 1)[1]).lower() in ALLOWED_EXTENSIONS


def post_student():
    card_image = request.files['card_image']
    if card_image:
        now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        random_num = random.randint(0, 100)
        card_image_name = secure_filename(str(now_time) + str(random_num) + '.' + card_image.filename.rsplit('.', 1)[1])
        card_image.save(os.path.join(current_app.config['CARD_IMAGE_PATH'], card_image_name))
    return jsonify('test upload')
