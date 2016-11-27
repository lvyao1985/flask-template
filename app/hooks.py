# -*- coding: utf-8 -*-

from . import db


def connect_db():
    """
    建立数据库连接
    :return:
    """
    db.connect()


def close_db(response):
    """
    关闭数据库连接
    :param response:
    :return:
    """
    if not db.is_closed():
        db.close()
