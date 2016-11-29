# -*- coding: utf-8 -*-

from functools import wraps

from flask import g, abort


def login_required(f):
    """
    需要登录
    :param f:
    :return:
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not g.user:
            abort(401)

        return f(*args, **kwargs)

    return wrapper
