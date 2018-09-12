# -*- coding: utf-8 -*-

__author__ = 'Jackie'

from django.db import models


class Question(models.Model):
    title = models.CharField(u"标题", max_length=128, blank=False, db_index=True)
    content = models.TextField(u"问题内容")
    src_url = models.URLField(u"抓取源路径", db_index=True)
    count_answer = models.IntegerField(u"回答量", db_index=True)
    count_view = models.IntegerField(u"浏览量", db_index=True)
    weight = models.IntegerField(u"权重", db_index=True)  # 回答量*10+浏览量
    speed_view = models.FloatField(u"每小时浏览增长量", db_index=True, null=True)
    create_time = models.DateTimeField(u"记录时间", auto_now_add=True)  # 是数据入库的时间,不一定是抓取时间
    crawl_time = models.DateTimeField(u"最后爬取时间", null=True)


class UpdateLog(models.Model):
    question = models.ForeignKey(Question)
    count_answer = models.IntegerField(u"回答量", db_index=True)
    count_view = models.IntegerField(u"浏览量", db_index=True)
    crawl_time = models.DateTimeField(u"抓取时间")


class QuestionKeyword(models.Model):
    question = models.ForeignKey(Question)
    keyword = models.CharField(u"关键字(文本)", max_length=32, db_index=True)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    content = models.TextField(u"回答内容")
    is_accepted = models.BooleanField(u"被采纳", default=False, db_index=True)
