# -*- coding: utf-8 -*-

from flask import request, session, g, url_for, redirect

from ...models import Admin
from ...constants import CMS_ADMIN_SESSION_KEY


def before_request():
    """
    请求前钩子函数
    :return:
    """
    endpoint = request.endpoint.split('.')[-1]
    g.admin = Admin.query_by_id(session.get(CMS_ADMIN_SESSION_KEY))  # g.admin
    if endpoint in ['login'] and g.admin:
        return redirect(url_for('.index'))

    elif endpoint not in ['login', 'static'] and not g.admin:
        return redirect(url_for('.login'))
