# -*- coding: utf-8 -*-

import datetime

from flask import current_app
from peewee import *
from playhouse.shortcuts import model_to_dict
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .constants import DEFAULT_PER_PAGE


_to_set = (lambda r: set(r) if r else set())
_nullable_strip = (lambda s: s.strip() or None if s else None)


class BaseModel(Model):
    """
    所有model的基类
    """
    id = PrimaryKeyField()
    create_time = DateTimeField(default=datetime.datetime.now)  # 创建时间
    update_time = DateTimeField(default=datetime.datetime.now)  # 更新时间
    weight = IntegerField(default=0)  # 排序权重

    class Meta:
        database = db
        only_save_dirty = True

    @classmethod
    def _exclude_fields(cls):
        """
        转换为dict表示时排除在外的字段
        :return:
        """
        return {'create_time', 'update_time'}

    @classmethod
    def _extra_attributes(cls):
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
        根据查询条件计数
        :param select_query: [SelectQuery or None]
        :return:
        """
        cnt = 0
        try:
            if select_query is None:
                select_query = cls.select()
            cnt = select_query.count()
        finally:
            return cnt

    @classmethod
    def iterator(cls, select_query=None, order_by=None, page=None, per_page=None):
        """
        根据查询条件返回迭代器
        :param select_query: [SelectQuery or None]
        :param order_by: [iterable or None]
        :param page:
        :param per_page:
        :return:
        """
        try:
            if select_query is None:
                select_query = cls.select()

            if order_by:
                _fields = cls._meta.fields
                clauses = []
                for item in order_by:
                    desc, attr = item.startswith('-'), item.lstrip('+-')
                    if attr in cls._exclude_fields():
                        continue
                    if attr in cls._extra_attributes():
                        attr = attr.split('_', 1)[-1]
                    if attr in _fields:
                        clauses.append(_fields[attr].desc() if desc else _fields[attr])
                if clauses:
                    select_query = select_query.order_by(*clauses)

            if page or per_page:
                select_query = select_query.paginate(int(page or 1), int(per_page or DEFAULT_PER_PAGE))

            return select_query.naive().iterator()

        except Exception, e:
            current_app.logger.error(e)
            return iter([])

    def to_dict(self, only=None, exclude=None, recurse=False, backrefs=False, max_depth=None):
        """
        转换为dict表示
        :param only: [iterable or None]
        :param exclude: [iterable or None]
        :param recurse: [bool]
        :param backrefs: [bool]
        :param max_depth:
        :return:
        """
        try:
            only = _to_set(only)
            exclude = _to_set(exclude) | self._exclude_fields()

            _fields = self._meta.fields
            only_fields = {_fields[k] for k in only if k in _fields}
            exclude_fields = {_fields[k] for k in exclude if k in _fields}
            extra_attrs = self._extra_attributes() - exclude
            if only:
                extra_attrs &= only
                if not only_fields:
                    exclude_fields = _fields.values()

            return model_to_dict(self, recurse=recurse, backrefs=backrefs, only=only_fields, exclude=exclude_fields,
                                 extra_attrs=extra_attrs, max_depth=max_depth)

        except Exception, e:
            current_app.logger.error(e)
            return {}

    def modified_fields(self, exclude=None):
        """
        与数据库中对应的数据相比，数值有变动的字段名称列表
        :param exclude: [iterable or None]
        :return:
        """
        try:
            exclude = _to_set(exclude)
            db_obj = self.query_by_id(self.id)
            return filter(lambda f: getattr(self, f) != getattr(db_obj, f) and f not in exclude,
                          self._meta.sorted_field_names)

        except Exception, e:
            current_app.logger.error(e)
            return None

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
    name = CharField(max_length=20, unique=True)  # 用户名
    password = CharField()  # 密码
    phone = CharField(null=True)  # 手机号码
    openid = CharField(null=True)  # 微信服务号openid
    last_login = DateTimeField(null=True)  # 最近登录时间
    last_ip = CharField(null=True)  # 最近登录IP
    authority = BigIntegerField(default=0)  # 权限

    class Meta:
        db_table = 'admin'

    @classmethod
    def _exclude_fields(cls):
        return BaseModel._exclude_fields() | {'password', 'last_login'}

    @classmethod
    def _extra_attributes(cls):
        return BaseModel._extra_attributes() | {'iso_last_login'}

    @classmethod
    def query_by_name(cls, name):
        """
        根据用户名查询
        :param name:
        :return:
        """
        admin = None
        try:
            admin = cls.get(cls.name == name)
        finally:
            return admin

    @classmethod
    def create_admin(cls, name, password, phone=None, openid=None, authority=0):
        """
        创建管理员
        :param name:
        :param password:
        :param phone:
        :param openid:
        :param authority:
        :return:
        """
        try:
            return cls.create(
                name=name.strip(),
                password=generate_password_hash(password),
                phone=_nullable_strip(phone),
                openid=_nullable_strip(openid),
                authority=authority
            )

        except Exception, e:
            current_app.logger.error(e)
            return None

    def check_password(self, password):
        """
        核对密码
        :param password:
        :return:
        """
        return check_password_hash(self.password, password)

    def change_password(self, password):
        """
        修改密码
        :param password:
        :return:
        """
        try:
            self.password = generate_password_hash(password)
            self.update_time = datetime.datetime.now()
            self.save()
            return self

        except Exception, e:
            current_app.logger.error(e)
            return None

    def login(self, ip):
        """
        登录
        :param ip:
        :return:
        """
        try:
            self.last_login = datetime.datetime.now()
            self.last_ip = ip
            self.save()
            return self

        except Exception, e:
            current_app.logger.error(e)
            return None

    def iso_last_login(self):
        return self.last_login.isoformat() if self.last_login else None


class WeixinUser(BaseModel):
    """
    微信用户
    """
    openid = CharField()
    unionid = CharField(null=True)
    nickname = CharField(null=True)
    sex = IntegerField(null=True)
    country = CharField(null=True)
    province = CharField(null=True)
    city = CharField(null=True)
    headimgurl = CharField(null=True)
    subscribe = IntegerField(null=True)
    subscribe_time = IntegerField(null=True)
    language = CharField(null=True)
    remark = CharField(null=True)
    groupid = IntegerField(null=True)
    tagid_list = TextField(null=True)

    class Meta:
        db_table = 'weixin_user'

    @classmethod
    def _exclude_fields(cls):
        return BaseModel._exclude_fields() | {'tagid_list'}

    @classmethod
    def _extra_attributes(cls):
        return BaseModel._extra_attributes() | {'array_tagid_list'}

    @classmethod
    def query_by_openid(cls, openid):
        """
        根据openid查询
        :param openid:
        :return:
        """
        weixin_user = None
        try:
            weixin_user = cls.get(cls.openid == openid)
        finally:
            return weixin_user

    @classmethod
    def create_weixin_user(cls, openid, unionid=None, nickname=None, sex=None, country=None, province=None, city=None,
                           headimgurl=None, subscribe=None, subscribe_time=None, language=None, remark=None,
                           groupid=None, tagid_list=None, **kwargs):
        """
        创建微信用户
        :param openid:
        :param unionid:
        :param nickname:
        :param sex:
        :param country:
        :param province:
        :param city:
        :param headimgurl:
        :param subscribe:
        :param subscribe_time:
        :param language:
        :param remark:
        :param groupid:
        :param tagid_list: [iterable or None]
        :param kwargs:
        :return:
        """
        try:
            return cls.create(
                openid=openid.strip(),
                unionid=_nullable_strip(unionid),
                nickname=_nullable_strip(nickname),
                sex=sex,
                country=_nullable_strip(country),
                province=_nullable_strip(province),
                city=_nullable_strip(city),
                headimgurl=_nullable_strip(headimgurl),
                subscribe=subscribe,
                subscribe_time=subscribe_time,
                language=_nullable_strip(language),
                remark=_nullable_strip(remark),
                groupid=groupid,
                tagid_list=','.join(map(str, tagid_list)) if tagid_list else None
            )

        except Exception, e:
            current_app.logger.error(e)
            return None

    def update_weixin_user(self, subscribe, unionid=None, nickname=None, sex=None, country=None, province=None,
                           city=None, headimgurl=None, subscribe_time=None, language=None, remark=None, groupid=None,
                           tagid_list=None, **kwargs):
        """
        更新微信用户
        :param subscribe:
        :param unionid:
        :param nickname:
        :param sex:
        :param country:
        :param province:
        :param city:
        :param headimgurl:
        :param subscribe_time:
        :param language:
        :param remark:
        :param groupid:
        :param tagid_list: [iterable or None]
        :param kwargs:
        :return:
        """
        try:
            self.subscribe = subscribe
            if subscribe:
                self.unionid = _nullable_strip(unionid)
                self.nickname = _nullable_strip(nickname)
                self.sex = sex
                self.country = _nullable_strip(country)
                self.province = _nullable_strip(province)
                self.city = _nullable_strip(city)
                self.headimgurl = _nullable_strip(headimgurl)
                self.subscribe_time = subscribe_time
                self.language = _nullable_strip(language)
                self.remark = _nullable_strip(remark)
                self.groupid = groupid
                self.tagid_list = ','.join(map(str, tagid_list)) if tagid_list else None
            if self.modified_fields():
                self.update_time = datetime.datetime.now()
                self.save()
            return self

        except Exception, e:
            current_app.logger.error(e)
            return None

    def array_tagid_list(self):
        return map(int, self.tagid_list.split(',')) if self.tagid_list else []


class WeixinPayOrder(BaseModel):
    """
    微信支付订单
    """
    class Meta:
        db_table = 'weixin_pay_order'


class WeixinPayRefund(BaseModel):
    """
    微信支付退款
    """
    class Meta:
        db_table = 'weixin_pay_refund'


class User(BaseModel):
    """
    用户
    """
    class Meta:
        db_table = 'user'


models = [Admin]
