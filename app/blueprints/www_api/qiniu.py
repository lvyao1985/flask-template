# -*- coding: utf-8 -*-

from flask import current_app, g
import qiniu

from . import bp_www_api
from ...api_utils import *
from utils.key_util import generate_random_key
from utils.qiniu_util import get_upload_token
from utils.weixin_util import get_temp_image_media


@bp_www_api.route('/qiniu/weixin_temp_images/', methods=['POST'])
def upload_weixin_temp_image_to_qiniu():
    """
    上传微信临时图片素材到七牛
    :return:
    """
    media_id = g.json.get('media_id')
    claim_args(1401, media_id)
    claim_args_string(1402, media_id)
    image = get_temp_image_media(current_app.config['WEIXIN'], media_id)
    claim_args_true(1803, image)

    key = generate_random_key(20, 'img_')
    upload_token = get_upload_token(current_app.config['QINIU'], key)
    claim_args_true(1850, upload_token)
    resp, info = qiniu.put_data(upload_token, key, image)
    claim_args_true(1851, resp and resp.get('key') == key)
    data = {
        'url': 'http://%s/%s' % (current_app.config['QINIU']['domain'], key)
    }
    return api_success_response(data)
