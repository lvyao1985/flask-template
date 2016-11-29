# -*- coding: utf-8 -*-

from flask import Blueprint

from ...api_utils import *
from .hooks import before_request


bp_www_api = Blueprint('bp_www_api', __name__)


bp_www_api.register_error_handler(APIException, handle_api_exception)
bp_www_api.register_error_handler(400, handle_400_error)
bp_www_api.register_error_handler(401, handle_401_error)
bp_www_api.register_error_handler(500, handle_500_error)
bp_www_api.before_request(before_api_request)
bp_www_api.before_request(before_request)
