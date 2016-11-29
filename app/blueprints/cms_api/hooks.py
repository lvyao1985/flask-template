# -*- coding: utf-8 -*-

from flask import session, g, abort

from ...models import Admin
from ...constants import CMS_ADMIN_SESSION_KEY


def before_request():
    """
    请求前钩子函数
    :return:
    """
    g.admin = Admin.query_by_id(session.get(CMS_ADMIN_SESSION_KEY))  # g.admin
    if not g.admin:
        abort(401)
