# -*- coding: utf-8 -*-

__author__ = 'Jackie'

"""
ITeye
http://www.iteye.com/problems/solved
@note: 貌似不再更新了,有反爬
"""

from pyquery import PyQuery as PQ
from base import QACrawl

ACTIVE = False


class Crawl_Iteye(QACrawl):
    TIME_SLEEP_INTERVAL = 5
    MAX_PAGE = 1455
    BASE_URL = "http://www.iteye.com"
    PAGE_URL = "http://www.iteye.com/problems/solved?page=%s"

    def extract_detail_url(self, html):
        pq = PQ(html)
        div = pq("div[class='question-summary']")
        hrefs = list()
        for a in div('h3 a'):
            href = PQ(a).attr('href')
            if href.startswith('/'):
                href = self.BASE_URL + href
            hrefs.append(href)
        return hrefs

    def analyse_detail_page(self, html):
        pq = PQ(html)
        div = pq('#main')
        title = div('div[class="problem problem_g"] h3:eq(0)').text()
        question = div('div[class="new_content"]').text()
        tags = list(PQ(a).text() for a in div('.ask_label>.tags>a'))
        answer = (div('.accept_solution div[class="solution solution_dd"]').text(), True)
        return dict(
            title=title,
            content=question,
            tags=tags,
            answers=[answer, ],
        )


def run():
    Crawl_Iteye().start()


if __name__ == "__main__":
    run()
