from flask import Blueprint
from . import views

main = Blueprint('main', __name__)

main.add_url_rule('/media/<path:path>', view_func=views.media, methods=['GET'])
