# -*- coding: utf-8 -*-
import urllib
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from django.db.models import Count
from common.paginator import Pt
from mz_crawl.models import Question, QuestionKeyword, Answer


def get_tags(top=None, page=1, per_page=25):
    """
    获取热门标签
    :param top: 例如top10
    :return:[(keyword,count),]
    """
    _list = list()
    objs = QuestionKeyword.objects.values('keyword').annotate(c_keyword=Count('question'))
    objs = objs.order_by('-c_keyword')
    total = 1
    if isinstance(top, int):
        objs = objs[:top]
    else:
        pg = Pt(objs, per_page=per_page).page(page)
        objs, page, total = pg.objects, pg.current, pg.total
    for obj in objs:
        _list.append(
            dict(
                name=obj['keyword'], count=obj['c_keyword'],
                url=reverse("crawl:questions") + "?tag=" + urllib.quote_plus(obj['keyword'].encode('utf8')),
            )
        )
    return _list, page, total


def get_tags_by_qid(qid):
    objs = QuestionKeyword.objects.filter(question_id=qid)
    tags = list(
        dict(name=t.keyword,
             url=reverse("crawl:questions") + "?tag=" + urllib.quote_plus(t.keyword.encode('utf8'))
             )
        for t in objs
    )
    return tags


def get_questions(tag=None, page=1, per_page=15):
    """
    根据标签获取问题列表
    :param tag: 标签关键字,str
    :param top: 例如top10,int or None,如果有此值,不分页
    :return:
    """
    if isinstance(tag, (str, unicode)):
        objs = QuestionKeyword.objects.values('question__id', 'question__title')
        objs = objs.filter(keyword=tag)
        objs = objs.order_by('-question__weight')
        pg = Pt(objs, per_page=per_page).page(page)
        data = list(
            dict(id=obj['question__id'], title=obj['question__title'])
            for obj in pg.objects
        )
        return data, pg.current, pg.total
    else:
        objs = Question.objects.values('id', 'title')
        objs = objs.order_by('-weight')
        pg = Pt(objs, per_page=per_page).page(page)
        data = list(
            dict(id=obj['id'], title=obj['title'])
            for obj in pg.objects
        )
        return data, pg.current, pg.total


def get_answers_by_qid(qid):
    """获取答案"""
    objs = Answer.objects.filter(question_id=qid).order_by('-is_accept')
    return objs


def get_top_questions_by_tag(tag=None, top=10):
    """
    获取tag下的top10
    :param tag: 标签
    :param top: top-X
    :return:
    """
    return get_questions(tag=tag, page=1, per_page=top)[0]


def get_question(qid):
    """根据问题ID"""
    object = get_object_or_404(Question, id=qid)
    return object
