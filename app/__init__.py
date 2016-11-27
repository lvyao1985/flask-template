# -*- coding: utf-8 -*-

from flask import Flask
from peewee import MySQLDatabase
from redis import StrictRedis

from config import Config, config


db = MySQLDatabase(None)
redis_client = StrictRedis(**Config.REDIS)


def create_app(config_name):
    """
    创建flask应用对象
    :param config_name:
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init(**app.config['MYSQL'])

    from .models import models
    db.create_tables(models, safe=True)

    from .exceptions import APIException
    from .hooks import handle_api_exception, before_app_request, after_app_request
    app.register_error_handler(APIException, handle_api_exception)
    app.before_request(before_app_request)
    app.teardown_request(after_app_request)

    from .misc import url_for_each_page
    app.jinja_env.globals['url_for_each_page'] = url_for_each_page

    from .blueprints.www_main import bp_www_main
    from .blueprints.www_api import bp_www_api
    from .blueprints.cms_main import bp_cms_main
    from .blueprints.cms_api import bp_cms_api
    app.register_blueprint(bp_www_main, subdomain=app.config['SUBDOMAIN'].get('www_main'))
    app.register_blueprint(bp_www_api, subdomain=app.config['SUBDOMAIN'].get('www_api'), url_prefix='/api')
    app.register_blueprint(bp_cms_main, subdomain=app.config['SUBDOMAIN'].get('cms_main'))
    app.register_blueprint(bp_cms_api, subdomain=app.config['SUBDOMAIN'].get('cms_api'), url_prefix='/api')

    return app
