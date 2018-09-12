# -*- coding: utf-8 -*-

__author__ = 'Jackie'

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', "mz_crawl.views.index", name="index"),
    url(r'^tags/$', "mz_crawl.views.tag_list_page", name="tags"),
    url(r'^questions/$', "mz_crawl.views.question_list_page", name="questions"),
    url(r'^q/(?P<qid>\d+)/$', "mz_crawl.views.question_detail_page", name="question"),
)
