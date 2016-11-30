# -*- coding: utf-8 -*-

from flask import Blueprint


bp_www_main = Blueprint('bp_www_main', __name__, static_folder='static')


from . import extensions
