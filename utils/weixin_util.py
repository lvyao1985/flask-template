# -*- coding: utf-8 -*-

import time
import json
import hashlib

import requests

from app import redis_client
from .key_util import generate_random_key


def get_access_token(wx):
    """
    获取微信access_token
    :param wx: [dict]
    :return:
    """
    app_id, app_secret = map(wx.get, ('app_id', 'app_secret'))
    if not (app_id and app_secret):
        return

    key = 'wx:%s:access_token' % app_id
    access_token = redis_client.get(key)
    if access_token:
        return access_token

    wx_url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {
        'grant_type': 'client_credential',
        'appid': app_id,
        'secret': app_secret
    }
    resp_json = requests.get(wx_url, params=params).json()
    access_token, expires_in = map(resp_json.get, ('access_token', 'expires_in'))
    if not (access_token and expires_in):
        return

    redis_client.set(key, access_token)
    redis_client.expire(key, int(expires_in) - 600)  # 提前10分钟更新access_token
    return access_token


def get_jsapi_ticket(wx):
    """
    获取微信jsapi_ticket
    :param wx: [dict]
    :return:
    """
    app_id, app_secret = map(wx.get, ('app_id', 'app_secret'))
    if not (app_id and app_secret):
        return

    key = 'wx:%s:jsapi_ticket' % app_id
    jsapi_ticket = redis_client.get(key)
    if jsapi_ticket:
        return jsapi_ticket

    access_token = get_access_token(wx)
    if not access_token:
        return

    wx_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket'
    params = {
        'access_token': access_token,
        'type': 'jsapi'
    }
    resp_json = requests.get(wx_url, params=params).json()
    jsapi_ticket, expires_in = map(resp_json.get, ('ticket', 'expires_in'))
    if not (jsapi_ticket and expires_in):
        return

    redis_client.set(key, jsapi_ticket)
    redis_client.expire(key, int(expires_in) - 600)  # 提前10分钟更新jsapi_ticket
    return jsapi_ticket


def get_user_info(wx, openid):
    """
    获取微信用户基本信息
    :param wx: [dict]
    :param openid:
    :return:
    """
    access_token = get_access_token(wx)
    if not access_token:
        return

    wx_url = 'https://api.weixin.qq.com/cgi-bin/user/info'
    params = {
        'access_token': access_token,
        'openid': openid,
        'lang': 'zh_CN'
    }
    resp = requests.get(wx_url, params=params)
    resp.encoding = 'utf-8'
    info = resp.json()
    if not info.get('errcode'):
        return info


def get_user_info_with_authorization(wx, code):
    """
    获取微信用户基本信息（网页授权）
    :param wx: [dict]
    :param code:
    :return:
    """
    app_id, app_secret = map(wx.get, ('app_id', 'app_secret'))
    if not (app_id and app_secret):
        return

    # 通过code换取网页授权access_token
    wx_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    params = {
        'appid': app_id,
        'secret': app_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    resp_json = requests.get(wx_url, params=params).json()
    access_token, openid, refresh_token = map(resp_json.get, ('access_token', 'openid', 'refresh_token'))
    if not (access_token and openid):
        return

    # # 检验access_token是否有效
    # wx_url = 'https://api.weixin.qq.com/sns/auth'
    # params = {
    #     'access_token': access_token,
    #     'openid': openid
    # }
    # resp_json = requests.get(wx_url, params=params).json()
    # if resp_json.get('errcode'):
    #     if not refresh_token:
    #         return
    #
    #     # 刷新access_token
    #     wx_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token'
    #     params = {
    #         'appid': app_id,
    #         'grant_type': 'refresh_token',
    #         'refresh_token': refresh_token
    #     }
    #     resp_json = requests.get(wx_url, params=params).json()
    #     access_token, openid = map(resp_json.get, ('access_token', 'openid'))
    #     if not (access_token and openid):
    #         return

    # 拉取用户信息
    wx_url = 'https://api.weixin.qq.com/sns/userinfo'
    params = {
        'access_token': access_token,
        'openid': openid,
        'lang': 'zh_CN'
    }
    resp = requests.get(wx_url, params=params)
    resp.encoding = 'utf-8'
    info = resp.json()
    if not info.get('errcode'):
        return info


def get_temp_image_media(wx, media_id):
    """
    获取微信临时图片素材
    :param wx: [dict]
    :param media_id:
    :return:
    """
    access_token = get_access_token(wx)
    if not access_token:
        return

    wx_url = 'https://api.weixin.qq.com/cgi-bin/media/get'
    params = {
        'access_token': access_token,
        'media_id': media_id
    }
    resp = requests.get(wx_url, params=params)
    content_type = resp.headers.get('Content-Type')
    if content_type and content_type.startswith('image/'):
        return resp.content


def send_custom_message(wx, openid, msg_type, msg_data):
    """
    发送微信客服消息
    :param wx: [dict]
    :param openid:
    :param msg_type:
    :param msg_data: [dict]
    :return:
    """
    access_token = get_access_token(wx)
    if not access_token:
        return

    wx_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send'
    params = {
        'access_token': access_token
    }
    data = {
        'touser': str(openid),
        'msgtype': str(msg_type),
        str(msg_type): msg_data
    }
    return requests.post(wx_url, params=params, data=json.dumps(data, ensure_ascii=False)).json()


def send_template_message(wx, openid, template_id, msg_data, url=''):
    """
    发送微信模板消息
    :param wx: [dict]
    :param openid:
    :param template_id:
    :param msg_data: [dict]
    :param url:
    :return:
    """
    access_token = get_access_token(wx)
    if not access_token:
        return

    wx_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send'
    params = {
        'access_token': access_token
    }
    data = {
        'touser': str(openid),
        'template_id': str(template_id),
        'url': str(url),
        'data': msg_data
    }
    return requests.post(wx_url, params=params, data=json.dumps(data, ensure_ascii=False)).json()


def create_menu(wx, buttons):
    """
    创建微信自定义菜单
    :param wx: [dict]
    :param buttons: [list]
    :return:
    """
    access_token = get_access_token(wx)
    if not access_token:
        return

    wx_url = 'https://api.weixin.qq.com/cgi-bin/menu/create'
    params = {
        'access_token': access_token
    }
    data = {
        'button': buttons
    }
    return requests.post(wx_url, params=params, data=json.dumps(data, ensure_ascii=False)).json()


def generate_qrcode_with_scene(wx, action, scene, expires=30):
    """
    生成微信带参数的二维码
    :param wx: [dict]
    :param action: 'QR_SCENE' - 临时二维码，'QR_LIMIT_SCENE' - 永久二维码，'QR_LIMIT_STR_SCENE' - 字符串参数值永久二维码
    :param scene:
    :param expires:
    :return:
    """
    access_token = get_access_token(wx)
    if not access_token:
        return

    wx_url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create'
    params = {
        'access_token': access_token
    }
    data = {
        'action_name': str(action),
        'action_info': {
            'scene': {'scene_str': str(scene)} if action == 'QR_LIMIT_STR_SCENE' else {'scene_id': int(scene)}
        }
    }
    if scene == 'QR_SCENE':
        data['expire_seconds'] = int(expires)
    resp_json = requests.post(wx_url, params=params, data=json.dumps(data, ensure_ascii=False)).json()
    ticket = resp_json.get('ticket')
    if not ticket:
        return

    wx_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode'
    params = {
        'ticket': ticket
    }
    resp = requests.get(wx_url, params=params)
    content_type = resp.headers.get('Content-Type')
    if content_type and content_type.startswith('image/'):
        return resp.content


def generate_pay_sign(wx, data):
    """
    生成微信支付签名
    :param wx: [dict]
    :param data: [dict]
    :return:
    """
    pay_key = wx.get('pay_key')
    if not pay_key:
        return

    items = ['%s=%s' % (k, data[k]) for k in sorted(data) if data[k]]
    items.append('key=%s' % pay_key)
    return hashlib.md5('&'.join(items).encode('utf-8')).hexdigest().upper()


def generate_jsapi_pay_params(wx, prepay_id):
    """
    生成微信公众号支付参数（WeixinJSBridge对象getBrandWCPayRequest参数）
    :param wx: [dict]
    :param prepay_id:
    :return:
    """
    params = {
        'appId': wx.get('app_id'),
        'timeStamp': str(int(time.time())),
        'nonceStr': generate_random_key(16),
        'package': 'prepay_id=%s' % prepay_id,
        'signType': 'MD5'
    }
    params['paySign'] = generate_pay_sign(wx, params)
    return params
