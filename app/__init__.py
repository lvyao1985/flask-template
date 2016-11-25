# -*- coding: utf-8 -*-

from flask import Flask
from peewee import MySQLDatabase
from redis import StrictRedis
from celery import Celery

from config import Config, config


db = MySQLDatabase(None)
redis_client = StrictRedis(**Config.REDIS)
celery = Celery(__name__)


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
    celery.conf.update(app.config)
    return app
