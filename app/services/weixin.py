# -*- coding: utf-8 -*-

from flask import current_app, url_for
import requests
import xmltodict

from utils.key_util import generate_random_key
from utils.weixin_util import generate_pay_sign


def unified_order(order):
    """
    微信支付统一下单
    :param order:
    :return:
    """
    if order.prepay_id:
        return

    wx = current_app.config['WEIXIN']
    params = order.to_dict(only=('device_info', 'body', 'detail', 'attach', 'out_trade_no', 'fee_type', 'total_fee',
                                 'spbill_create_ip', 'time_start', 'time_expire', 'goods_tag', 'trade_type',
                                 'product_id', 'limit_pay', 'openid'))
    params['appid'] = wx.get('app_id')
    params['mch_id'] = wx.get('mch_id')
    params['nonce_str'] = generate_random_key(16)
    params['notify_url'] = url_for('bp_www_main.weixin_pay_notify', _external=True)
    params['sign'] = generate_pay_sign(wx, params)
    xml = current_app.jinja_env.get_template('weixin/pay/unified_order.xml').render(**params)
    wx_url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    resp = requests.post(wx_url, data=xml.encode('utf-8'), headers={'Content-Type': 'application/xml; charset="utf-8"'})
    resp.encoding = 'utf-8'
    try:
        result = xmltodict.parse(resp.text)['xml']
        sign = result.pop('sign')
        assert sign == generate_pay_sign(wx, result), u'微信支付签名验证失败'
        order.update_order_result(result)
    except Exception, e:
        current_app.logger.error(e)
        current_app.logger.info(resp.text)
