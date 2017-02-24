# -*- coding: utf-8 -*-

from celery.signals import task_prerun, task_postrun

from . import db, create_celery_app


celery = create_celery_app()


@task_prerun.connect()
def celery_prerun(sender=None, task=None, task_id=None, *args, **kwargs):
    """
    celery任务执行前钩子函数
    :param sender:
    :param task:
    :param task_id:
    :param args:
    :param kwargs:
    :return:
    """
    if db.is_closed():
        db.connect()


@task_postrun.connect()
def celery_postrun(sender=None, task=None, task_id=None, retval=None, state=None, *args, **kwargs):
    """
    celery任务执行后钩子函数
    :param sender:
    :param task:
    :param task_id:
    :param retval:
    :param state:
    :param args:
    :param kwargs:
    :return:
    """
    if not db.is_closed():
        db.close()
