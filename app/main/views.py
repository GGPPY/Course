# coding=utf-8
import os

from flask import current_app, send_from_directory


def media(path):
    basedir = current_app.config['BASEDIR']
    media_path = os.path.join(basedir, 'media')
    return send_from_directory(media_path, path)
