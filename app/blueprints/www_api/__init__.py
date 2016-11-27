# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify

from ...exceptions import APIException


bp_www_api = Blueprint('bp_www_api', __name__)


@bp_www_api.errorhandler(500)
def handle_500(e):
    """
    处理500错误
    :param e:
    :return:
    """
    e = APIException(1000)
    return jsonify(e.to_dict()), e.status_code
