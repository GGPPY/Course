from flask import Blueprint
from . import models

course = Blueprint('course', __name__, url_prefix='/course')
