# -*- coding: utf-8 -*-

__author__ = 'Jackie'

"""
博客园
http://q.cnblogs.com/
已解决
"""

import re
from pyquery.pyquery import PyQuery as PQ
from base import QACrawl

ACTIVE = True


class Craw_Cnblogs(QACrawl):
    METHOD = QACrawl.METHOD_MTQ
    MAX_PAGE = 160
    BASE_URL = "http://q.cnblogs.com"
    PAGE_URL = "http://q.cnblogs.com/list/solved?page=%s"

    def analyse_detail_page(self, html):
        """分析详情页"""
        pq = PQ(html)
        div = pq('#main')
        data = dict()
        data['title'] = div('h1>a').text()
        data['content'] = div('#qes_content').text()
        data['tags'] = list(PQ(a).text() for a in div('#d_tag>a'))
        data['answers'] = [(div("div[class='qitem_item qclear']>.q_content").text(), True), ]
        try:
            qid = re.search('\d+', div('h1>a').attr('href')).group()
        except:
            qid = None
        data['count_view'] = 0 if qid is None else \
            self.post("http://q.cnblogs.com/q/GetQuestonViewCount/", data={'qid': qid}) or 0
        try:
            data['count_answer'] = int(
                re.search(
                    u'\d+', div('#panelAnswerList .title_green').text()
                ).group()) + 1
        except:
            data['count_answer'] = 1

        return data

    def extract_detail_url(self, html):
        """
        分析列表页面,解析出detail url
        :param content:
        :return:list of detail url
        """
        hrefs = list()
        for a in PQ(html)('.news_entry>a'):
            href = PQ(a).attr('href').strip()
            if href.startswith('/'):
                href = self.BASE_URL + href
            hrefs.append(href)
        return hrefs


def run():
    Craw_Cnblogs().start()


if __name__ == "__main__":
    run()
