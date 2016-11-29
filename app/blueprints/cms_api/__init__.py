# -*- coding: utf-8 -*-

from flask import Blueprint

from ...api_utils import *


bp_cms_api = Blueprint('bp_cms_api', __name__)


bp_cms_api.register_error_handler(APIException, handle_api_exception)
bp_cms_api.register_error_handler(400, handle_400)
bp_cms_api.register_error_handler(500, handle_500)
bp_cms_api.before_request(before_api_request)
