# -*- coding: utf-8 -*-

import os


class Config:
    """
    flask应用对象配置
    """
    _project_name = 'flask-template'
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

    # mysql
    DATABASE = {
        'engine': 'peewee.MySQLDatabase',
        'charset': 'utf8mb4',
        'host': 'localhost',
        'port': 3306,
        'user': os.getenv('FLASK_MYSQL_USER'),
        'passwd': os.getenv('FLASK_MYSQL_PASSWD'),
        'name': os.getenv('FLASK_MYSQL_DB') or _project_name
    }

    # redis
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = int(os.getenv('FLASK_REDIS_DB') or 0)

    # 七牛
    QINIU = {
        'access_key': os.getenv('QINIU_ACCESS_KEY'),
        'secret_key': os.getenv('QINIU_SECRET_KEY'),
        'bucket': os.getenv('QINIU_BUCKET'),
        'domain': os.getenv('QINIU_DOMAIN')
    }

    # celery
    BROKER_URL = 'redis://localhost:6379/%s' % (os.getenv('FLASK_CELERY_BROKER') or 0)
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/%s' % (os.getenv('FLASK_CELERY_BACKEND') or 0)

    # 云片
    YUNPIAN = {
        'key': os.getenv('YUNPIAN_KEY'),
        'single_send': 'https://sms.yunpian.com/v2/sms/single_send.json',
        'batch_send': 'https://sms.yunpian.com/v2/sms/batch_send.json'
    }

    # 微信服务号
    WEIXIN = {
        'id': os.getenv('WEIXIN_ID'),
        'app_id': os.getenv('WEIXIN_APP_ID'),
        'app_secret': os.getenv('WEIXIN_APP_SECRET'),
        'token': os.getenv('WEIXIN_TOKEN'),
        'mch_id': os.getenv('WEIXIN_MCH_ID'),
        'pay_key': os.getenv('WEIXIN_PAY_KEY'),
        'cert_path': os.getenv('WEIXIN_CERT_PATH'),
        'key_path': os.getenv('WEIXIN_KEY_PATH')
    }

    def __init__(self):
        pass


class DevelopmentConfig(Config):
    """
    开发环境配置
    """
    DEBUG = True
    SERVER_NAME = 'lvh.me:8888'
    SUBDOMAIN = {
        'www_main': None,
        'www_api': None,
        'cms_main': 'cms',
        'cms_api': 'cms'
    }


class TestingConfig(Config):
    """
    测试环境配置
    """
    TESTING = True
    SERVER_NAME = ''
    SUBDOMAIN = {
        'www_main': Config._project_name,
        'www_api': Config._project_name,
        'cms_main': '%s-cms' % Config._project_name,
        'cms_api': '%s-cms' % Config._project_name
    }
    _extensions_domain = '%s.%s' % (SUBDOMAIN['www_main'], SERVER_NAME) if SUBDOMAIN['www_main'] else SERVER_NAME
    WEIXIN_USER_LOGIN_URL = 'http://%s/extensions/weixin/user/login/' % _extensions_domain
    WEIXIN_ORDER_NOTIFY_URL = 'http://%s/extensions/weixin/order/notify/' % _extensions_domain


class ProductionConfig(Config):
    """
    生产环境配置
    """
    SERVER_NAME = ''
    SUBDOMAIN = {
        'www_main': None,
        'www_api': None,
        'cms_main': 'cms',
        'cms_api': 'cms'
    }
    _extensions_domain = '%s.%s' % (SUBDOMAIN['www_main'], SERVER_NAME) if SUBDOMAIN['www_main'] else SERVER_NAME
    WEIXIN_USER_LOGIN_URL = 'http://%s/extensions/weixin/user/login/' % _extensions_domain
    WEIXIN_ORDER_NOTIFY_URL = 'http://%s/extensions/weixin/order/notify/' % _extensions_domain


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
