# -*- coding: utf-8 -*-

import time
import hashlib

from flask import current_app, request

from . import bp_www_api
from ...api_utils import *
from utils.key_util import generate_random_key
from utils.weixin_util import get_jsapi_ticket


@bp_www_api.route('/weixin/js_sdk_config/', methods=['GET'])
def get_weixin_js_sdk_config():
    """
    获取微信JS-SDK权限验证配置信息
    :return:
    """
    url = request.args.get('url')
    claim_args(1201, url)
    wx = current_app.config['WEIXIN']
    jsapi_ticket = get_jsapi_ticket(wx)
    claim_args(1802, jsapi_ticket)

    noncestr = generate_random_key(16)
    timestamp = int(time.time())
    items = ['jsapi_ticket=%s' % jsapi_ticket, 'noncestr=%s' % noncestr, 'timestamp=%s' % timestamp, 'url=%s' % url]
    items.sort()
    signature = hashlib.sha1('&'.join(items)).hexdigest()
    data = {
        'app_id': wx.get('app_id'),
        'noncestr': noncestr,
        'timestamp': timestamp,
        'signature': signature
    }
    return api_success_response(data)
