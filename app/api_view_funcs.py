# -*- coding: utf-8 -*-

from flask import request, g

from .api_utils import *


__all__ = [
    'list_objects',
    'get_object',
    'update_object_weight',
    'delete_object',
    'delete_objects'
]


def list_objects(model, mark='objects'):
    """
    列出全部对象
    :param model:
    :param mark:
    :return:
    """
    order_by, page, per_page = map(request.args.get, ('order_by', 'page', 'per_page'))
    order_by = order_by.split(',') if order_by else None
    claim_args_digits_string(1202, *filter(None, (page, per_page)))

    data = {
        mark: [obj.to_dict(g.fields) for obj in model.iterator(None, order_by, page, per_page)],
        'total': model.count()
    }
    return api_success_response(data)


def get_object(_id, model, mark='object'):
    """
    获取单个对象
    :param _id:
    :param model:
    :param mark:
    :return:
    """
    obj = model.query_by_id(_id)
    claim_args(1104, obj)

    data = {
        mark: obj.to_dict(g.fields)
    }
    return api_success_response(data)


def update_object_weight(_id, model, mark='object'):
    """
    修改对象权重
    :param _id:
    :param model:
    :param mark:
    :return:
    """
    weight = g.json.get('weight')
    obj = model.query_by_id(_id)
    claim_args(1104, obj)
    claim_args(1401, weight)
    claim_args_int(1402, weight)

    data = {
        mark: obj.change_weight(weight).to_dict(g.fields)
    }
    return api_success_response(data)


def delete_object(_id, model):
    """
    删除单个对象
    :param _id:
    :param model:
    :return:
    """
    obj = model.query_by_id(_id)
    claim_args(1104, obj)

    obj.delete_instance(recursive=True)
    return api_success_response({})


def delete_objects(model):
    """
    删除多个对象
    :param model:
    :return:
    """
    ids = request.args.get('ids')
    claim_args(1601, ids)
    ids = ids.split(',')
    claim_args_digits_string(1602, *ids)
    objs = map(model.query_by_id, ids)
    claim_args(1602, *objs)

    for obj in objs:
        obj.delete_instance(recursive=True)
    return api_success_response({})
