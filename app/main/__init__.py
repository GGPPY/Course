# coding=utf-8
from flask import Blueprint
from . import views

main = Blueprint('main', __name__)

media = Blueprint('media', __name__)

media.add_url_rule('/media/<path:path>', view_func=views.media, methods=['GET'])

# 学员报名
apply_course = views.StudentView.as_view('apply')
main.add_url_rule('/apply/query', view_func=apply_course, methods=["GET"])
main.add_url_rule('/apply', view_func=apply_course, methods=["POST"])
main.add_url_rule('/apply/update', view_func=apply_course, methods=["PUT"])
