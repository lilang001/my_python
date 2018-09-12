# -*- coding: utf-8 -*-

from django.http.response import HttpResponse
from django.shortcuts import render
import interface

__author__ = 'Jackie'


def recommend_video(request):
    """推荐视频资源"""
    # url = request.POST.get('url')
    html = request.POST.get('html', 'jandroidandroidandroidajavavapython,java,co,pythondcco')
    code, data = interface.get_fit_video(html)
    if code:
        resp = render(request, 'mz_plus/video.html', data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        return HttpResponse(u'hello')


def index(request):
    resp = render(request, "mz_plus/test.html")
    return resp
