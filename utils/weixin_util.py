# -*- coding: utf-8 -*-

import hashlib

import requests

from app import redis_client


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
