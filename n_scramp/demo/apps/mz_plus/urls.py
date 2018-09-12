# -*- coding: utf-8 -*-

__author__ = 'Jackie'

from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index),
    url(r'^recommend_video/$', views.recommend_video)
)
