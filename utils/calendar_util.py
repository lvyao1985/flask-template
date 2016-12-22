# -*- coding: utf-8 -*-

import calendar


def calc_day(year, month, n, weekday):
    """
    计算指定的月份中第n个weekday是当月的第几天
    :param year:
    :param month:
    :param n:
    :param weekday: 0 - Monday, ..., 6 - Sunday
    :return:
    """
    first, days = calendar.monthrange(year, month)
    options = range(1 + 7 * (n - 1), 1 + 7 * n)
    day = options[weekday - first]
    if day <= days:
        return day
