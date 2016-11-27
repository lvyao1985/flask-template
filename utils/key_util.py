# -*- coding: utf-8 -*-

import string
import random


def generate_random_key(length, starts='', mode='uld'):
    """
    生成随机字符串
    :param length:
    :param starts:
    :param mode: u - uppercase letters, l - lowercase letters, d - digits
    :return:
    """
    letters = ''
    if 'u' in mode:
        letters += string.ascii_uppercase
    if 'l' in mode:
        letters += string.ascii_lowercase
    if 'd' in mode:
        letters += string.digits
    return starts + ''.join([random.choice(letters) for i in range(0, length - len(starts))]) if letters else starts
