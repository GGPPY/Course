# coding=utf-8
from flask import Blueprint
from . import views

course = Blueprint('course', __name__, url_prefix='/course')


course.add_url_rule('/apply', view_func=views.course_apply, methods=['POST'])

# 科目增删改查
subject = views.SubjectView.as_view('subject')
course.add_url_rule('/subject', view_func=subject, methods=["GET", "POST"])
course.add_url_rule('/subject/<int:subject_id>', view_func=subject, methods=["PUT", "DELETE"])

# 课程增删改查
c = views.CourseView.as_view('c')
course.add_url_rule('', view_func=c, methods=["GET", "POST"])
course.add_url_rule('/<int:course_id>', view_func=c, methods=["PUT", "DELETE"])

