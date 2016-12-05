# -*- coding: utf-8 -*-

from flask import session, g, abort

from ...models import Admin
from ...constants import CMS_ADMIN_SESSION_KEY


def admin_authentication():
    """
    管理员身份认证
    :return:
    """
    g.admin = Admin.query_by_id(session.get(CMS_ADMIN_SESSION_KEY))  # g.admin
    if not g.admin:
        abort(401)
