# -*- coding: utf-8 -*-

import time

from flask import current_app, request, session, g, abort

from ...models import Admin
from ...constants import ADMIN_SESSION_KEY, ADMIN_TOKEN_TAG
from utils.des import decrypt


# def admin_authentication():
#     """
#     管理员身份认证
#     :return:
#     """
#     g.admin = Admin.query_by_id(session.get(ADMIN_SESSION_KEY))  # g.admin
#     if not g.admin:
#         abort(401)


def admin_authentication():
    """
    管理员身份认证
    :return:
    """
    if request.endpoint.split('.')[-1] in ['login']:
        return

    token = request.environ.get('HTTP_AUTHORIZATION')
    if not token:
        abort(401)

    try:
        tag, admin_id, expires = decrypt(token).split(':')
        expires = int(expires)
    except Exception, e:
        current_app.logger.error(e)
        abort(401)

    if tag != ADMIN_TOKEN_TAG or expires < time.time():
        abort(401)

    g.admin = Admin.query_by_id(admin_id)  # g.admin
    if not g.admin:
        abort(401)
