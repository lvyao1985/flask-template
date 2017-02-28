# -*- coding: utf-8 -*-

from os import environ
from logging.handlers import RotatingFileHandler
import logging


class Config:
    """
    配置
    """
    _project_name = 'flask-template'  # TODO: 项目名称
    SECRET_KEY = environ.get('FLASK_SECRET_KEY')

    # mysql
    MYSQL = {
        'charset': 'utf8mb4',
        'host': 'localhost',
        'port': 3306,
        'user': environ.get('FLASK_MYSQL_USER'),
        'password': environ.get('FLASK_MYSQL_PASSWORD'),
        'database': environ.get('FLASK_MYSQL_DB') or _project_name.replace('-', '_')
    }

    # redis
    REDIS = {
        'host': 'localhost',
        'port': 6379,
        'db': int(environ.get('FLASK_REDIS_DB') or 0)
    }

    # celery
    BROKER_URL = 'amqp://%s:%s@localhost:5672/%s' % (environ.get('CELERY_BROKER_USER'),
                                                     environ.get('CELERY_BROKER_PASSWORD'),
                                                     environ.get('CELERY_BROKER_VHOST') or _project_name)
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/%s' % (environ.get('CELERY_BACKEND_DB') or 0)
    CELERY_TASK_SERIALIZER = 'pickle'
    CELERY_ACCEPT_CONTENT = ['pickle']
    CELERY_RESULT_SERIALIZER = 'pickle'
    CELERY_TIMEZONE = 'Asia/Shanghai'

    # 七牛
    QINIU = {
        'access_key': environ.get('QINIU_ACCESS_KEY'),
        'secret_key': environ.get('QINIU_SECRET_KEY'),
        'bucket': environ.get('QINIU_BUCKET'),
        'domain': environ.get('QINIU_DOMAIN')
    }

    # 云片
    YUNPIAN = {
        'key': environ.get('YUNPIAN_KEY'),
        'single_send': 'https://sms.yunpian.com/v2/sms/single_send.json',
        'batch_send': 'https://sms.yunpian.com/v2/sms/batch_send.json'
    }

    # 微信服务号
    WEIXIN = {
        'id': environ.get('WEIXIN_ID'),
        'app_id': environ.get('WEIXIN_APP_ID'),
        'app_secret': environ.get('WEIXIN_APP_SECRET'),
        'token': environ.get('WEIXIN_TOKEN'),
        'aes_key': environ.get('WEIXIN_AES_KEY'),
        'mch_id': environ.get('WEIXIN_MCH_ID'),
        'pay_key': environ.get('WEIXIN_PAY_KEY'),
        'cert_path': environ.get('WEIXIN_CERT_PATH'),
        'key_path': environ.get('WEIXIN_KEY_PATH')
    }

    def __init__(self):
        pass

    @staticmethod
    def init_app(app):
        """
        初始化flask应用对象
        :param app:
        :return:
        """
        file_handler = RotatingFileHandler('backend.log', maxBytes=1024 * 1024 * 100, backupCount=10, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(
            logging.Formatter(u'[%(asctime)s] - %(pathname)s (%(lineno)s) - [%(levelname)s] - %(message)s'))
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)


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
    SERVER_NAME = ''  # TODO: 域名
    SUBDOMAIN = {
        'www_main': Config._project_name,
        'www_api': Config._project_name,
        'cms_main': '%s-cms' % Config._project_name,
        'cms_api': '%s-cms' % Config._project_name
    }


class ProductionConfig(Config):
    """
    生产环境配置
    """
    SERVER_NAME = ''  # TODO: 域名
    SUBDOMAIN = {
        'www_main': None,
        'www_api': None,
        'cms_main': 'cms',
        'cms_api': 'cms'
    }


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
