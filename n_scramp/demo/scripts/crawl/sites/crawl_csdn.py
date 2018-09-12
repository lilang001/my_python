# -*- coding: utf-8 -*-
import re

__author__ = 'Jackie'

"""
CSDN
http://ask.csdn.net/
"""

from pyquery.pyquery import PyQuery as PQ
from base import QACrawl

ACTIVE = True


class Craw_CSDN(QACrawl):
    METHOD = QACrawl.METHOD_MT
    MAX_PAGE = 1578
    BASE_URL = "http://ask.csdn.net"
    PAGE_URL = "http://ask.csdn.net/?page=%s&type=resolved"

    def analyse_detail_page(self, html):
        pq = PQ(html)
        div = pq('.questions_detail_con')
        data = dict()
        data['title'] = div('dt').text()
        data['content'] = div('dd').text()
        data['tags'] = list(PQ(a).text() for a in div('.tags>a'))
        data['answers'] = [(pq('.answer_accept>div:eq(0)').text(), True), ]
        try:
            text = pq('div[class="answer_sort_con  q_operate"] p:eq(0)').text()
            data['count_answer'] = int(re.search(u"(\d+)个回答", text).groups()[0])
        except:
            data['count_answer'] = 1
        try:
            text = div.next('div a:eq(1)').text()
            data['count_view'] = int(re.search(u"浏览(\d+)", text).groups()[0])
        except:
            data['count_view'] = 1

        return data

    def extract_detail_url(self, html):
        """
        分析列表页面,解析出detail url
        :param content:
        :return:list of detail url
        """
        hrefs = list()
        for a in PQ(html)('.questions_detail_con>dl>dt>a'):
            href = PQ(a).attr('href').strip()
            if href.startswith('/'):
                href = self.BASE_URL + href
            hrefs.append(href)
        return hrefs


def run():
    Craw_CSDN().start()


if __name__ == "__main__":
    run()
