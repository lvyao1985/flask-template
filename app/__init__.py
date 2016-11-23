# -*- coding: utf-8 -*-

import os

from flask import Flask

from .config import config


# 初始化flask应用对象
app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_CONFIG') or 'default'])
