# -*- coding: utf-8 -*-

from flask import request, session, g, url_for, redirect, flash, render_template

from . import bp_cms_main
from ...models import Admin
from ...constants import ADMIN_SESSION_KEY


@bp_cms_main.route('/', methods=['GET'])
def index():
    """
    首页
    :return:
    """
    return render_template('cms/index.html')


@bp_cms_main.route('/login/', methods=['GET', 'POST'])
def login():
    """
    管理员登录
    :return:
    """
    if request.method == 'GET':
        return render_template('cms/login.html')

    if request.method == 'POST':
        name, password = map(request.form.get, ('name', 'password'))
        admin = Admin.query_by_name(name)
        if admin and admin.check_password(password):
            session[ADMIN_SESSION_KEY] = admin.id
            admin.login(g.ip)
            flash(u'登录成功', 'info')
            return redirect(url_for('.index'))

        flash(u'请输入正确的用户名和密码', 'error')
        return redirect(url_for('.login'))


@bp_cms_main.route('/logout/', methods=['GET'])
def logout():
    """
    管理员退出
    :return:
    """
    session.pop(ADMIN_SESSION_KEY, None)
    return redirect(url_for('.login'))
