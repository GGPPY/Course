from flask import Blueprint
from . import views

course = Blueprint('course', __name__, url_prefix='/course')

course.add_url_rule('/test', view_func=views.post_student, methods=['POST'])
