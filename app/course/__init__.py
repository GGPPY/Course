# coding=utf-8
from flask import Blueprint
from . import views

course = Blueprint('course', __name__)


course.add_url_rule('/apply', view_func=views.course_apply, methods=['POST'])

# 科目增删改查
subject = views.SubjectView.as_view('subject')
course.add_url_rule('/subject', view_func=subject, methods=["GET", "POST"])
course.add_url_rule('/subject/<int:subject_id>', view_func=subject, methods=["PUT", "DELETE"])

# 课程增删改查
lesson = views.CourseView.as_view('lesson')
course.add_url_rule('/course', view_func=lesson, methods=["GET", "POST"])
course.add_url_rule('/course/<int:course_id>', view_func=lesson, methods=["PUT", "DELETE"])

# 学生增删改查
student = views.StudentView.as_view('student')
course.add_url_rule('/student', view_func=student, methods=["GET", "POST"])
course.add_url_rule('/student/<int:student_id>', view_func=student, methods=['PUT', 'DELETE'])
