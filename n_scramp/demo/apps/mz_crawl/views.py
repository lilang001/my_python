# -*- coding: utf-8 -*-

"""
@author : Jackie
@date : 2015/10/30
@note :
"""
import urllib
from django.core.urlresolvers import reverse
from django.shortcuts import render

import interface


def index(request):
    """首页展示热门标签"""
    tags, page, total = interface.get_tags(top=20)
    for d in tags:
        d['url'] = d['url'] + "&show=top10"
    return render(
        request, "mz_crawl/index.html",
        dict(tags=tags)
    )


def tag_list_page(request):
    """所有标签"""
    page = request.GET.get('page')
    tags, page, total = interface.get_tags(page=page, per_page=20)

    return render(
        request, "mz_crawl/t_list.html",
        dict(tags=tags, current_page=page, sum_page=total)
    )


def question_list_page(request):
    """问题列表页"""
    tag = request.GET.get('tag')
    show = request.GET.get('show')
    page = request.GET.get('page')
    total = 0
    if tag is not None:
        if show == "top10":
            data = interface.get_top_questions_by_tag(tag=tag, top=10)
        else:
            data, page, total = interface.get_questions(tag=tag, page=page, per_page=20)
    else:
        data, page, total = interface.get_questions(page=page, per_page=20)[0]

    return render(
        request, "mz_crawl/q_list.html",
        dict(questions=data,
             tag=tag, title="Top-10" if show == "top10" else "",
             current_page=page,
             sum_page=total,
             )
    )


def question_detail_page(request, qid):
    """问题详情页"""
    question = interface.get_question(qid)
    answers = question.answer_set.all().order_by('-is_accepted')
    tags = interface.get_tags_by_qid(qid)
    return render(
        request, "mz_crawl/q_detail.html",
        dict(q=question,
             answers=answers,
             tags=tags)
    )
