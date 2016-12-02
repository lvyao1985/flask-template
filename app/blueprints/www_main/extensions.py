# -*- coding: utf-8 -*-

import hashlib

from flask import current_app, request, make_response, jsonify
import xmltodict

from . import bp_www_main
from utils.qiniu_util import get_upload_token


@bp_www_main.route('/extensions/qiniu/upload_token/', methods=['GET'])
def get_qiniu_upload_token():
    """
    获取七牛上传凭证
    :return:
    """
    data = {
        'uptoken': get_upload_token(current_app.config['QINIU'])
    }
    return jsonify(data)


@bp_www_main.route('/extensions/weixin/api/', methods=['GET', 'POST'])
def weixin_api():
    """
    （由微信调用）微信API
    :return:
    """
    signature, timestamp, nonce = map(request.args.get, ('signature', 'timestamp', 'nonce'))
    if not all((signature, timestamp, nonce)):
        current_app.logger.error(u'微信API验证参数不完整')
        return make_response('')

    items = [current_app.config['WEIXIN']['token'], timestamp, nonce]
    items.sort()
    hashcode = hashlib.sha1(''.join(items)).hexdigest()
    if hashcode != signature:
        current_app.logger.error(u'微信API验证失败')
        return make_response('')

    if request.method == 'GET':
        current_app.logger.info(u'微信API验证成功')
        return make_response(request.args.get('echostr', ''))

    if request.method == 'POST':
        xml = ''
        try:
            message = xmltodict.parse(request.data)['xml']
            current_app.logger.info(message)
        except Exception, e:
            current_app.logger.error(e)
        finally:
            return make_response(xml)
