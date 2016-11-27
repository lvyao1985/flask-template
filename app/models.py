# -*- coding: utf-8 -*-

import datetime

from peewee import *

from . import db


class BaseModel(Model):
    """
    所有model的基类；包含以下字段：id，创建时间，更新时间，排序权重
    """
    id = PrimaryKeyField()
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)
    weight = IntegerField(default=0)

    class Meta:
        database = db


class Admin(BaseModel):
    """
    管理员
    """
    class Meta:
        db_table = 'admin'


models = [Admin]
