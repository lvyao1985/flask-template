# -*- coding: utf-8 -*-

import time

from flask import current_app, request, g

from ...models import WeixinUser, User
from ...constants import WEIXIN_USER_COOKIE_KEY, USER_TOKEN_TAG
from app import redis_client
from utils.des import decrypt
from utils.weixin_util import get_user_info


def weixin_user_authentication():
    """
    微信用户身份认证
    :return:
    """
    g.user = None  # g.user
    token = request.cookies.get(WEIXIN_USER_COOKIE_KEY)
    if not token:
        return

    try:
        weixin_user_id = decrypt(token)
    except Exception, e:
        current_app.logger.error(e)
        return

    g.user = WeixinUser.query_by_id(weixin_user_id)
    if not g.user:
        return

    key = 'wx:user:%s:info' % g.user.id
    if redis_client.get(key) != 'off':
        redis_client.set(key, 'off')
        redis_client.expire(key, 7200)  # 每隔两小时更新微信用户基本信息
        info = get_user_info(current_app.config['WEIXIN'], g.user.openid)
        if info:
            g.user.update_weixin_user(**info)


def user_authentication():
    """
    用户身份认证
    :return:
    """
    g.user = None  # g.user
    token = request.environ.get('HTTP_AUTHORIZATION')
    if not token:
        return

    try:
        tag, user_id, expires = decrypt(token).split(':')
        expires = int(expires)
    except Exception, e:
        current_app.logger.error(e)
        return

    if tag != USER_TOKEN_TAG or expires < time.time():
        return

    g.user = User.query_by_id(user_id)
