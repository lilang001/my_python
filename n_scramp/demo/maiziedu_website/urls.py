# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^plus/', include('mz_plus.urls', namespace='plus')),
    url(r'^crawl/', include('mz_crawl.urls', namespace='crawl')),
)
