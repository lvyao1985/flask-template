# -*- coding: utf-8 -*-

from flask import Blueprint

from .hooks import admin_authentication


bp_cms_main = Blueprint('bp_cms_main', __name__, static_folder='static')


bp_cms_main.before_request(admin_authentication)


from . import extensions, views
