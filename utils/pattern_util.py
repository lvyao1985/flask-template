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
    检查手机号码格式是否正确
    :param phone:
    :return:
    """
    return bool(re.match(r'1[34578]\d{9}$', phone))


def check_email(email):
    """
    检查电子邮箱格式是否正确
    :param email:
    :return:
    """
    return bool(re.match(r'\S+@\S+\.\S+$', email))


def check_id_card(id_card):
    """
    检查身份证号码格式是否正确
    :param id_card:
    :return:
    """
    return bool(re.match(r'[1-9]\d{5}[12]\d{3}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[0-9xX]$', id_card)
                or re.match(r'[1-9]\d{7}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}$', id_card))
