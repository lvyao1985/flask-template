# -*- coding: utf-8 -*-

import hashlib
import time

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
        return None

    key = 'wx:%s:access_token' % app_id
    access_token = redis_client.get(key)
    if access_token:
        return access_token

    wx_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' \
             % (app_id, app_secret)
    resp_json = requests.get(wx_url).json()
    access_token, expires_in = map(resp_json.get, ('access_token', 'expires_in'))
    if not (access_token and expires_in):
        return None

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
        return None

    key = 'wx:%s:jsapi_ticket' % app_id
    jsapi_ticket = redis_client.get(key)
    if jsapi_ticket:
        return jsapi_ticket

    access_token = get_access_token(wx)
    if not access_token:
        return None

    wx_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % access_token
    resp_json = requests.get(wx_url).json()
    jsapi_ticket, expires_in = map(resp_json.get, ('ticket', 'expires_in'))
    if not (jsapi_ticket and expires_in):
        return None

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
        return None

    wx_url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (access_token, openid)
    resp = requests.get(wx_url)
    resp.encoding = 'utf-8'
    info = resp.json()
    if info.get('errcode'):
        return None

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
        return None

    # 通过code换取网页授权access_token
    wx_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s' \
             '&grant_type=authorization_code' % (app_id, app_secret, code)
    resp_json = requests.get(wx_url).json()
    access_token, openid, refresh_token = map(resp_json.get, ('access_token', 'openid', 'refresh_token'))
    if not (access_token and openid):
        return None

    # # 检验access_token是否有效
    # wx_url = 'https://api.weixin.qq.com/sns/auth?access_token=%s&openid=%s' % (access_token, openid)
    # resp_json = requests.get(wx_url).json()
    # if resp_json.get('errcode'):
    #     if not refresh_token:
    #         return None
    #
    #     # 刷新access_token
    #     wx_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=%s&grant_type=refresh_token' \
    #              '&refresh_token=%s' % (app_id, refresh_token)
    #     resp_json = requests.get(wx_url).json()
    #     access_token, openid = map(resp_json.get, ('access_token', 'openid'))
    #     if not (access_token and openid):
    #         return None

    # 拉取用户信息
    wx_url = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (access_token, openid)
    resp = requests.get(wx_url)
    resp.encoding = 'utf-8'
    info = resp.json()
    if info.get('errcode'):
        return None

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
        return None

    wx_url = 'https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s' % (access_token, media_id)
    resp = requests.get(wx_url)
    if not resp.headers['Content-Type'].startswith('image/'):
        return None

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
        return None

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
