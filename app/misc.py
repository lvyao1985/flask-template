# -*- coding: utf-8 -*-

from flask import request, url_for, jsonify


def api_success_response(data):
    """
    API请求成功的响应
    :param data: [dict]
    :return:
    """
    return jsonify({'code': 0, 'message': 'Success', 'data': data})


def url_for_each_page(page):
    """
    生成各个分页的URL
    :param page:
    :return:
    """
    args = dict(request.view_args.items() + request.args.to_dict(flat=False).items())
    args['page'] = page if page > 1 else None
    return url_for(request.endpoint, **args)
