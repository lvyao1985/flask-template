# -*- coding: utf-8 -*-

from flask import Blueprint

from ...api_utils import *


bp_www_api = Blueprint('bp_www_api', __name__)


bp_www_api.register_error_handler(APIException, handle_api_exception)
bp_www_api.register_error_handler(400, handle_400)
bp_www_api.register_error_handler(500, handle_500)
bp_www_api.before_request(before_api_request)
