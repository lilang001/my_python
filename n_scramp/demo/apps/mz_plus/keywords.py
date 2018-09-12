# -*- coding: utf-8 -*-

import re

__author__ = 'Jackie'

DEFAULT_KEY_WORD = 'python'
KEYWORDS = [
    'android',
    'java',
    'php',
    'python',
    'web',
    'html',
    'bootstrap'
]


def _init():
    """初始化,从课程分类表中取出所有分类,作为关键字"""
    from mz_course.models import CourseCatagory
    objs = CourseCatagory.objects.all().values('name')
    if objs:
        global KEYWORDS
        del KEYWORDS[:]
        for obj in objs:
            KEYWORDS.append(obj['name'])


_init()


def extrac_keyword(content):
    """
    检测内容中的关键字,提取出现次数最多的
    :param content:
    :to-do: 性能优化,正则提前编译,排除标签和链接
    :return:
    """
    _tmp = list()
    for k in KEYWORDS:
        _tmp.append((k, len(re.findall(re.escape(k), content, re.I | re.M))))
    _tmp.sort(key=lambda x: x[1], reverse=True)

    return _tmp[0][0] if _tmp[0][1] else DEFAULT_KEY_WORD
