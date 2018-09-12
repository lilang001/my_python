# -*- coding: utf-8 -*-

"""
@author : Jackie
@date : 2015/11/2
@note :
"""
import re
import threading
from billiard import Queue
import requests
from pyquery.pyquery import PyQuery as PQ
import logging
import time

logging.basicConfig(format='%(asctime)s %(message)s ---------- %(module)s.%(funcName)s Line:%(lineno)d',
                    # %(pathname)s:
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)

logger = logging.getLogger("ass")
logger.setLevel(logging.INFO)


def get_list_page():
    pages = list()

    resp = requests.get("http://www.youdaili.net/Daili/http/")
    pq = PQ(resp.text)
    ass = pq('.newslist_line>li>a')
    for a in ass[:3]:
        new_url = pq(a).attr('href')
        resp = requests.get(new_url)
        pq = PQ(resp.text)

        text = pq('.dede_pages>ul>li:eq(0)>a').html()
        num_pages = int(re.search("共(\d+)页", text).groups()[0])

        pages.append(new_url)
        for n in range(2, num_pages + 1):
            pages.append(new_url[:-5] + "_" + str(n) + ".html")
    return pages


def scra_list_page(pages):
    ret = list()
    for page_url in pages:
        pq = PQ(url=page_url)
        ret.extend(re.findall(r"(?P<ip>\d+\.\d+\.\d+\.\d+)\:(?P<port>\d+)@(?P<pro>\w+)#", pq.text()))
    return ret


queue = Queue()
all = list()


def test_proxy():
    while 1:
        try:
            p = queue.get_nowait()
        except:
            break
        proxies = {
            p[2].lower(): '%s:%s' % (p[0], p[1]),
        }
        try:
            begin = time.time()
            code = requests.get("http://www.google.com.hk/", proxies=proxies, timeout=5).status_code
            cost = int((time.time() - begin) * 1000)
            all.append(list(p) + [cost, ])
            logger.info("%s,%s,%s" % (p, code, cost))
        except:
            pass
            # logger.error("%s,%s" % (p, 'error'))


if __name__ == "__main__":
    pages = get_list_page()
    proxys = scra_list_page(pages)
    for p in proxys:
        queue.put(p)
    ths = [threading.Thread(target=test_proxy) for i in xrange(40)]
    for t in ths: t.start()
    for t in ths: t.join()

    print sorted(p, key=lambda x: x[-1])
