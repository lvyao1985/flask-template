# -*- coding: utf-8 -*-

from flask import request, g, abort

from . import db


def before_app_request():
    """
    请求前全局钩子函数
    :return:
    """
    if not (request.blueprint and request.endpoint):
        abort(404)

    g.ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')  # g.ip
    if db.is_closed():
        db.connect()


def after_app_request(resp):
    """
    请求后全局钩子函数
    :param resp:
    :return:
    """
    if not db.is_closed():
        db.close()
