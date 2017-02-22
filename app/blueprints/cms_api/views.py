# -*- coding: utf-8 -*-

import time

from flask import g

from . import bp_cms_api
from ...models import Admin
from ...api_utils import *
from ...constants import MIN_PASSWORD_LEN, MAX_PASSWORD_LEN, ADMIN_TOKEN_TAG, ADMIN_LOGIN_VALID_DAYS
from utils.des import encrypt


@bp_cms_api.route('/admin/login/', methods=['PUT'])
def login():
    """
    管理员登录
    :return:
    """
    name, password = map(g.json.get, ('name', 'password'))
    claim_args(1401, name, password)
    claim_args_string(1402, name, password)
    admin = Admin.query_by_name(name)
    claim_args_true(1403, admin)
    claim_args_true(1404, admin.check_password(password))

    token = encrypt('%s:%s:%s' % (ADMIN_TOKEN_TAG, admin.id, int(time.time()) + 86400 * ADMIN_LOGIN_VALID_DAYS))
    data = {
        'token': token,
        'admin': admin.to_dict(g.fields)
    }
    admin.login(g.ip)
    return api_success_response(data)


@bp_cms_api.route('/admin/password/', methods=['PUT'])
def update_admin_password():
    """
    修改管理员密码
    :return:
    """
    password_old, password_new = map(g.json.get, ('password_old', 'password_new'))
    claim_args(1401, password_old, password_new)
    claim_args_string(1402, password_old, password_new)
    claim_args_true(1404, g.admin.check_password(password_old))
    claim_args_true(1405, MIN_PASSWORD_LEN <= len(password_new) <= MAX_PASSWORD_LEN)

    admin = g.admin.change_password(password_new)
    data = {
        'admin': admin.to_dict(g.fields)
    }
    return api_success_response(data)
