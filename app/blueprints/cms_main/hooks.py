# -*- coding: utf-8 -*-

from flask import request, session, g, url_for, redirect

from ...models import Admin
from ...constants import ADMIN_SESSION_KEY


def admin_authentication():
    """
    管理员身份认证
    :return:
    """
    g.admin = Admin.query_by_id(session.get(ADMIN_SESSION_KEY))  # g.admin
    endpoint = request.endpoint.split('.')[-1]
    if endpoint in ['login'] and g.admin:
        return redirect(url_for('.index'))

    elif endpoint not in ['login', 'static'] and not g.admin:
        return redirect(url_for('.login'))
