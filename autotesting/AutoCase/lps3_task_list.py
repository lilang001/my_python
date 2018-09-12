# _*_ coding:utf-8 _*_
__author__ = 'Administrator'
import requests
import sqls
import time
from pyquery import PyQuery as pq
from Autotesing import settings
from mysql import select
from public import equal, Driver, content_deal, time_deal, login_by_res

class TaskList():
    def __init__(self):
        self.url = settings.SITE_URL + '/lps3/student/class/160/'

    def task_list(self):
        ses = login_by_res('18008062322', '11111111')
        txt = pq(ses.get(self.url).text)
        actual = list()
        for i in txt('#lineList>ul>li'):
            i = pq(i)
            stage_name = i('.zyStageTit').text()
            for j in i('.YaHei'):
                j = pq(j)
                task_name = j.text()
                actual.append((stage_name, task_name))
        expect = select(sqls.task_list)
        equal('task_list', expect, actual)

    def task__list_schedule(self):
        ses = login_by_res('18008062322', '11111111')
        txt = pq(ses.get(self.url).text)
        actual = list()
        for i in txt('#lineList>ul>li'):
            i = pq(i)
            stage_name = i('.zyStageTit').text()
            for j in i('.YaHei'):
                j = pq(j)
                task_name = j.text()
                actual.append((stage_name, task_name))
        expect = select(sqls.task_list)
        equal('task_list', expect, actual)


if __name__ == '__main__':
    TaskList().task__list_schedule()
