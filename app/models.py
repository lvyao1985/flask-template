# -*- coding: utf-8 -*-

import datetime

from flask import current_app
from peewee import *
from peewee import SelectQuery
from playhouse.shortcuts import model_to_dict

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
        only_save_dirty = True

    @classmethod
    def _exclude_fields(cls):
        """
        转换为dict表示时排除在外的字段
        :return:
        """
        return {cls.create_time, cls.update_time}

    @staticmethod
    def _extra_attributes():
        """
        转换为dict表示时额外增加的属性
        :return:
        """
        return {'iso_create_time', 'iso_update_time'}

    @classmethod
    def query_by_id(cls, _id):
        """
        根据id查询
        :param _id:
        :return:
        """
        obj = None
        try:
            obj = cls.get(cls.id == _id)
        finally:
            return obj

    @classmethod
    def count(cls, select_query=None):
        """
        根据查询语句计数
        :param select_query: [SelectQuery or None]
        :return:
        """
        cnt = 0
        try:
            select_query = select_query or cls.select()
            if isinstance(select_query, SelectQuery):
                cnt = select_query.count()
        finally:
            return cnt

    def to_dict(self, only_fields=None, exclude_fields=None, recurse=False, backrefs=False, max_depth=None):
        """
        转换为dict表示
        :param only_fields: [iterable or None]
        :param exclude_fields: [iterable or None]
        :param recurse: [bool]
        :param backrefs: [bool]
        :param max_depth:
        :return:
        """
        try:
            model = self.__class__
            only = set()
            exclude = model._exclude_fields()
            extra_attrs = model._extra_attributes()

            if only_fields:
                only.add(self._meta.primary_key)
                extra_attrs &= set(only_fields)
                for attr_name in only_fields:
                    f = getattr(model, attr_name, None)
                    if isinstance(f, Field):
                        only.add(f)

            if exclude_fields:
                for attr_name in exclude_fields:
                    f = getattr(model, attr_name, None)
                    if isinstance(f, Field):
                        exclude.add(f)

            return model_to_dict(self, recurse=recurse, backrefs=backrefs, only=only, exclude=exclude,
                                 extra_attrs=extra_attrs, max_depth=max_depth)

        except Exception, e:
            current_app.logger.error(e)
            return {}

    def change_weight(self, weight):
        """
        修改排序权重
        :param weight:
        :return:
        """
        try:
            self.weight = weight
            self.save()
            return self

        except Exception, e:
            current_app.logger.error(e)
            return None

    def iso_create_time(self):
        return self.create_time.isoformat()

    def iso_update_time(self):
        return self.update_time.isoformat()


class Admin(BaseModel):
    """
    管理员
    """
    class Meta:
        db_table = 'admin'


models = [Admin]
