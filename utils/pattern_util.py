# -*- coding: utf-8 -*-

import re


def is_alphabet(ustr):
    """
    判断一个unicode字符串是否全由英文字母组成
    :param ustr:
    :return:
    """
    for uchar in ustr:
        if not (u'\u0041' <= uchar <= u'\u005a' or u'\u0061' <= uchar <= u'\u007a'):
            return False

    return bool(ustr)


def check_phone(phone):
    """
    检查手机号码是否正确
    :param phone:
    :return:
    """
    return bool(re.match(r'1[34578]\d{9}$', phone))
