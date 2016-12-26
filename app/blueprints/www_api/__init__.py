# -*- coding: utf-8 -*-

from flask import Blueprint

from ...api_utils import *


bp_www_api = Blueprint('bp_www_api', __name__)


bp_www_api.register_error_handler(APIException, handle_api_exception)
bp_www_api.register_error_handler(400, handle_400_error)
bp_www_api.register_error_handler(401, handle_401_error)
bp_www_api.register_error_handler(403, handle_403_error)
bp_www_api.register_error_handler(404, handle_404_error)
bp_www_api.register_error_handler(500, handle_500_error)
bp_www_api.before_request(before_api_request)
# TODO: 请求前钩子函数，可从.hooks中选择


from . import qiniu, weixin
