# -*- coding: utf-8 -*-

import qiniu


def get_upload_token(qn, key=None):
    """
    获取七牛上传凭证
    :param qn: [dict]
    :param key:
    :return:
    """
    return qiniu.Auth(qn.get('access_key'), qn.get('secret_key')).upload_token(qn.get('bucket'), key=key)
