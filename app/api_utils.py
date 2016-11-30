# -*- coding: utf-8 -*-

import numbers

from flask import current_app, request, g, abort, jsonify


__all__ = [
    'APIException',
    'handle_api_exception',
    'handle_400_error',
    'handle_401_error',
    'handle_500_error',
    'before_api_request',
    'api_success_response',
    'claim_args',
    'claim_args_true',
    'claim_args_bool',
    'claim_args_string',
    'claim_args_digits_string',
    'claim_args_int',
    'claim_args_number',
    'claim_args_list',
    'claim_args_dict'
]


class APIException(Exception):
    """
    API异常
    """
    ERRORS = {
        1000: 'Internal Server Error',
        1100: 'Bad Request',
        1101: 'Unauthorized',
        1103: 'Forbidden',
        1104: 'Not Found',
        1201: u'GET方法url参数不完整',
        1202: u'GET方法url参数值不正确',
        1401: u'POST/PUT方法json数据不完整',
        1402: u'POST/PUT方法json数据值或类型不正确',
        1601: u'DELETE方法url参数不完整',
        1602: u'DELETE方法url参数值不正确'
    }
    status_code = 200

    def __init__(self, code, status_code=None):
        Exception.__init__(self)
        self.code = code
        self.message = self.ERRORS.get(code)
        if isinstance(status_code, int):
            self.status_code = status_code

    def to_dict(self):
        """
        转换为dict表示
        :return:
        """
        return {'code': self.code, 'message': self.message, 'data': {}}


def handle_api_exception(e):
    """
    处理APIException
    :param e:
    :return:
    """
    return jsonify(e.to_dict()), e.status_code


def handle_400_error(e):
    """
    处理400错误
    :param e:
    :return:
    """
    e = APIException(1100)
    return jsonify(e.to_dict()), e.status_code


def handle_401_error(e):
    """
    处理401错误
    :param e:
    :return:
    """
    e = APIException(1101)
    return jsonify(e.to_dict()), e.status_code


def handle_500_error(e):
    """
    处理500错误
    :param e:
    :return:
    """
    e = APIException(1000)
    return jsonify(e.to_dict()), e.status_code


def before_api_request():
    """
    API请求前钩子函数
    :return:
    """
    if request.method in ['POST', 'PUT']:
        if not request.is_json:
            abort(400)

        g.json = request.get_json()  # g.json
        current_app.logger.info(u'JSON: %s' % g.json)
    fields = request.args.get('fields')
    g.fields = fields.split(',') if fields else None  # g.fields


def api_success_response(data):
    """
    API请求成功的响应
    :param data: [dict]
    :return:
    """
    return jsonify({'code': 0, 'message': 'Success', 'data': data})


def claim_args(code, *args):
    for arg in args:
        if not (arg or isinstance(arg, (numbers.Number, bool))):
            raise APIException(code)


def claim_args_true(code, *args):
    for arg in args:
        if not arg:
            raise APIException(code)


def claim_args_bool(code, *args):
    for arg in args:
        if not isinstance(arg, bool):
            raise APIException(code)


def claim_args_string(code, *args):
    for arg in args:
        if not isinstance(arg, basestring):
            raise APIException(code)


def claim_args_digits_string(code, *args):
    for arg in args:
        if not (isinstance(arg, basestring) and arg.isdigit()):
            raise APIException(code)


def claim_args_int(code, *args):
    for arg in args:
        if not isinstance(arg, int):
            raise APIException(code)


def claim_args_number(code, *args):
    for arg in args:
        if not isinstance(arg, numbers.Real):
            raise APIException(code)


def claim_args_list(code, *args):
    for arg in args:
        if not isinstance(arg, list):
            raise APIException(code)


def claim_args_dict(code, *args):
    for arg in args:
        if not isinstance(arg, dict):
            raise APIException(code)
