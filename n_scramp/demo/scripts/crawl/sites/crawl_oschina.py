# -*- coding: utf-8 -*-
import re

__author__ = 'Jackie'

"""
开源中国
http://www.oschina.net/question?catalog=1
"""

from pyquery import PyQuery as PQ
from base import QACrawl

ACTIVE = True


class Crawl_Oschina(QACrawl):
    METHOD = QACrawl.METHOD_MT
    MAX_PAGE = 2861
    PAGE_URL = "http://www.oschina.net/question?catalog=1&show=time&p=%s"

    def extract_detail_url(self, html):
        pq = PQ(html)
        div = pq("div[class='question-detail']")
        hrefs = list()
        for a in div('a:eq(0)'):
            href = PQ(a).attr('href')
            hrefs.append(href)
        return hrefs

    def analyse_detail_page(self, html):
        pq = PQ(html)
        div = pq('.main')
        title = div('.QTitle a').text()
        question = div('.Content>.detail').text()
        tags = list(PQ(a).text() for a in div('#tags_nav a'))
        answers = list()
        for li in pq('.QuestionReplies li'):
            li = PQ(li)
            answer_content = li('.body .detail').text()
            vote_div = PQ(li.prev('div'))
            answer_accepted = True if vote_div('.accept-on') else False
            answers.append((answer_content, answer_accepted))
        try:
            text = pq('div[class="Asker special"] .pinfo>span:eq(1)').text()
            count_answer, count_view = re.search(u'(\d+) \u56de/(\d+)\u9605', text).groups()
        except:
            count_answer = 0
            count_view = 1

        return dict(
            title=title,
            content=question,
            tags=tags,
            answers=answers,
            count_answer=count_answer,
            count_view=count_view
        )


def run():
    Crawl_Oschina().start()


if __name__ == "__main__":
    run()
