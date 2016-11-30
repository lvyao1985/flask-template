# -*- coding: utf-8 -*-

from flask import Blueprint

from .hooks import before_request


bp_cms_main = Blueprint('bp_cms_main', __name__, static_folder='static')


bp_cms_main.before_request(before_request)


from . import extensions
