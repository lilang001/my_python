# -*- coding: utf-8 -*-

__author__ = 'Jackie'
"""
20线程跑
"""

import Queue
import os
import time
import datetime
import threading
import requests
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
import django

django.setup()

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) Gecko/20100101 Firefox/29.0"}
from mz_crawl import models


def time_cost(func):
    def wrapper(*args, **kwargs):
        begin = time.time()
        ret = func(*args, **kwargs)
        print func.func_code, "finish,cost:%s" % (time.time() - begin)
        return ret

    return wrapper


class ForbiddenException(Exception):
    pass


class ScraListThread(threading.Thread):
    """抓取列表页的线程"""

    def __init__(self, parent, name=None):
        threading.Thread.__init__(self, name=name)
        self.parent = parent
        self.queue_page = self.parent.queue_url_page
        self.queue = self.parent.queue_url_detail

    def run(self):
        while 1:
            try:
                page_url = self.queue_page.get(timeout=10)
                html = self.parent.get(page_url)
                if not html:
                    continue
                for href in self.parent.extract_detail_url(html):
                    self.queue.put(href)
            except:
                break
        print self.__class__, self.name, 'finish..'


class ScraDetailThread(threading.Thread):
    """抓取详情页的线程"""

    def __init__(self, parent, name=None):
        threading.Thread.__init__(self, name=name)
        self.parent = parent
        self.queue_url = self.parent.queue_url_detail
        self.queue_data = self.parent.queue_data_detail

    def run(self):
        while 1:
            try:
                url = self.parent.queue_url_detail.get(timeout=10)
            except Exception, e:
                break
            data = self.parent.analyse_detail_page(url)
            data['src_url'] = url
            data['crawl_time'] = datetime.datetime.now()
            self.queue_data.put(data)
        self.__class__, self.name, "finish.."


class SaveDataThread(threading.Thread):
    """数据保存线程"""

    def __init__(self, parent, name=None):
        threading.Thread.__init__(self, name=name)
        self.parent = parent
        self.queue = self.parent.queue_data_detail

    def run(self):
        while 1:
            try:
                data = self.queue.get(timeout=10)
            except:
                break
            self.parent.save(data)
        print self.__class__, self.name, "finish.."


class Request(object):
    TIME_SLEEP_RETRY = 3  # 重试时间粒度
    TIME_SLEEP_INTERVAL = 0  # 每次访问时间粒度

    def get(self, url):
        """如果连接超时,尝试10次"""
        try_times = 1
        # print 'get url: %s' % url
        while try_times <= 1:
            try:
                if self.TIME_SLEEP_INTERVAL:
                    time.sleep(self.TIME_SLEEP_INTERVAL)
                resp = requests.get(url, headers=headers, timeout=30)
                time.sleep(1)
                if resp.status_code == 200:
                    return resp.text
                elif resp.status_code == 403:
                    print 'failed:%s' % url
                    raise ForbiddenException(u"fuck,又被封了~~~%s" % url)
            except ForbiddenException, e:
                raise e
            except:
                time.sleep(self.TIME_SLEEP_RETRY)
            try_times += 1

    def post(self, url, data):
        try_times = 1
        # print 'post url: %s,%s' % (url, data)
        while try_times <= 1:
            try:
                if self.TIME_SLEEP_INTERVAL:
                    time.sleep(self.TIME_SLEEP_INTERVAL)
                resp = requests.post(url, data=data, headers=headers, timeout=30)
                time.sleep(1)
                if resp.status_code == 200:
                    return resp.text
                elif resp.status_code == 403:
                    print 'failed:%s' % url
                    raise ForbiddenException(u"fuck,又被封了~~~")
            except ForbiddenException, e:
                raise e
            except:
                time.sleep(self.TIME_SLEEP_RETRY)
            try_times += 1


class QACrawl(Request):
    METHOD_PT = 0  # 单线程模式
    METHOD_MT = 1  # 多线程流程模式,每个线程执行完整流程
    METHOD_MTQ = 2  # 多线程多任务模式
    METHOD = METHOD_MT

    MAX_PAGE = 1000
    PAGE_URL = '%s'

    last = set(d['src_url'] for d in models.Question.objects.all().values('src_url'))

    def __init__(self):
        self.queue_url_page = Queue.Queue()  # 列表页的url
        self.queue_url_detail = Queue.Queue()  # detail页的url
        self.queue_data_detail = Queue.Queue()  # 单页数据
        self.running = True

    def calc_weight(self, count_view, count_answer):
        return count_answer * 10 + count_view

    def save(self, data):
        """数据存储,目前为同步存储
        """
        if self.src_has_fetched(data.get('src_url')):
            self.update(data)
        transaction.set_autocommit(False, using='crawl')
        try:
            question = models.Question()
            question.title = data.get('title', '')
            question.content = data.get('content', '')
            question.src_url = data.get('src_url', '')
            question.count_view = int(data.get('count_view', 0))
            question.count_answer = int(data.get('count_answer', 0))
            question.crawl_time = data.get('crawl_time')
            question.weight = self.calc_weight(question.count_view, question.count_answer)
            question.save()
            for kw in data.get('tags'):
                qkw = models.QuestionKeyword()
                qkw.question = question
                qkw.keyword = kw
                qkw.save()
            for a_content, a_flag in data.get('answers', []):
                answer = models.Answer()
                answer.question = question
                answer.content = a_content
                answer.is_accepted = a_flag
                answer.save()
            transaction.commit(using='crawl')
        except Exception, e:
            transaction.rollback(using='crawl')
            print e
            print data

    def update(self, data):
        transaction.set_autocommit(False, using='crawl')
        try:
            question = models.Question.objects.get(data.get('src_url'))
            question.count_view = int(data.get('count_view', 0))
            question.count_answer = int(data.get('count_answer', 0))
            question.weight = self.calc_weight(question.count_view, question.count_answer)
            question.crawl_time = data.get('crawl_time')
            question.save()
            transaction.commit(using='crawl')
        except Exception, e:
            transaction.rollback(using='crawl')
            print e
            print data

    def extract_detail_url(self, html):
        """提取详情页的地址"""
        return ['%s-%s' % (html, i) for i in xrange(1, 6)]

    def analyse_detail_page(self, html):
        """分析详情页"""
        return dict(
            title='',
            question='',
            tags=list(),
            answer=list(),
            count_answer=0,
            count_views=0,
            weight=0,
        )

    def src_has_fetched(self, url):
        return url in self.last

    def fetch_one_page(self, url):
        html = self.get(url)
        for href in self.extract_detail_url(html):
            html = self.get(href)
            if not html:
                continue
            data = self.analyse_detail_page(html)
            data['src_url'] = href
            data['crawl_time'] = datetime.datetime.now()
            self.save(data)

    def run_st(self):
        """单线程跑"""
        page = 0
        while page < self.MAX_PAGE:
            page += 1
            url = self.PAGE_URL % page
            self.fetch_one_page(url)

    def run_mt(self):
        """多线程跑"""
        page = 0
        while page <= self.MAX_PAGE:
            tpool = []
            for i in xrange(60):
                page += 1
                if page > self.MAX_PAGE:
                    break
                url = self.PAGE_URL % page
                t = threading.Thread(target=self.fetch_one_page, args=(url,))
                tpool.append(t)
            for t in tpool:
                t.start()
            for t in tpool:
                t.join()

    def run_mtq(self):
        """多线程,分布,队列
        #TO-DO:阻塞了
        """
        page = 1
        while page <= self.MAX_PAGE:
            url = self.PAGE_URL % page
            self.queue_url_page.put(url)
            page += 1

        # 启动page页获取线程
        t0s = [ScraListThread(self) for i in range(20)]
        # 详情页获取线程
        t1s = [ScraDetailThread(self) for i in range(80)]
        # 数据存储线程
        t2s = [SaveDataThread(self) for i in range(2)]

        # 启动线程
        for t in t0s + t1s + t2s:
            t.start()
        # 等待线程结束
        for t in t0s + t1s + t2s:
            t.join()
        print self.queue_url_page.qsize(), self.queue_url_detail.qsize(), self.queue_url_detail.qsize()

    @time_cost
    def run(self):
        if self.METHOD == self.METHOD_MT:
            return self.run_mt()
        elif self.METHOD == self.METHOD_PT:
            return self.run_st()
        elif self.METHOD_MTQ == self.METHOD_MTQ:
            return self.run_mtq()
        else:
            pass

    def start(self):
        return self.run()


if __name__ == "__main__":
    QACrawl().start()
