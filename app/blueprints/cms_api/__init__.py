# -*- coding: utf-8 -*-

from flask import Blueprint

from .hooks import admin_authentication
from ...api_utils import *


bp_cms_api = Blueprint('bp_cms_api', __name__)


bp_cms_api.register_error_handler(APIException, handle_api_exception)
bp_cms_api.register_error_handler(400, handle_400_error)
bp_cms_api.register_error_handler(401, handle_401_error)
bp_cms_api.register_error_handler(403, handle_403_error)
bp_cms_api.register_error_handler(404, handle_404_error)
bp_cms_api.register_error_handler(500, handle_500_error)
bp_cms_api.before_request(before_api_request)
bp_cms_api.before_request(admin_authentication)


from . import views
