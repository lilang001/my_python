# _*_ coding:utf-8 _*_
__author__ = 'Administrator'

import requests
import sqls
import time
import threading
from pyquery import PyQuery as pq
from Autotesing import settings
from mysql import select
from public import equal, Driver, content_deal, time_deal
from selenium import webdriver

# 澳乐爬虫啪啪啪啪
def aole_test():
    f = open('lilang.txt', 'w')

    for i in xrange(1):
        url = 'http://www.itrip.com/aodaliya/wanle#/2'
        txt = requests.get(url).text.encode('ISO-8859-1', 'ignore').decode('UTF-8', 'ignore')
        title_list = pq(txt)('.mt15 .horiz ul li')
        a =list()
        for li_lang in title_list:
            li_lang = pq(li_lang)
            title = li_lang('.pro_title').text()
            price = li_lang('.js_curMonery_exten').text()
            a.append((title, price))
            f.writelines([title, '', price, '\n'])
        print (a)
    f.close()
# 检查指定url是否正常访问
def url_check():
    url = {'q.142.com:8000/', 'q.142.com:8000/ask/', 'q.142.com:8000/ask/tag/cpjl/', 'q.142.com:8000/ask/12535/',
           'q.142.com:8000/job/', 'q.142.com:8000/tech/', 'q.142.com:8000/news/',  'q.142.com:8000/lesson/',
           'q.142.com:8000/trend/', 'q.142.com:8000/tech/',
           'q.142.com:8000/job/', 'q.142.com:8000/tool/', 'q.142.com:8000/set/', 'q.142.com:8000/tag/81/',
           'q.142.com:8000/article/12562/', 'q.142.com:8000/party/', 'q.142.com:8000/party/12545/', 'q.142.com:8000/pcourse/',
           'q.142.com:8000/pcourse/12556/', 'q.142.com:8000/blog/', 'q.142.com:8000/common/dynmsg/5'}
    for i in url:
        i = 'http://q.142.com:8000/'+i.split('8000/')[-1]
        j = 'http://192.168.1.142/group/' + i.split('8000/')[-1]
        old = pq(requests.get(i).content)('title').text()
        new = pq(requests.get(j).content)('title').text()
        print (i), (j), old.encode('gbk'), new.encode('gbk')


def crash_lps3():
    s = requests.session()
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36",
           "Referer": "http://www.142.com/"}
    form_data = {'account_l': '18008062308', 'password_l': '11111111'}
    # post 换成登录的地址，
    s.post('http://www.142.com/user/login/', data=form_data, headers=header)
    # 换成抓取的地址
    count_200 = 0
    count_502 = 0
    count_504 = 0
    count_other = 0
    for i in range(30):
        txt = s.get('http://www.142.com/lps3/ea/stats/satisfaction/')
        if txt.status_code == 200:
            count_200 += 1
        elif txt.status_code == 502:
            count_502 += 1
        elif txt.status_code == 504:
            count_504 += 1
        else:
            count_other += 1
    print (count_200, count_502, count_504, count_other)

def test_time():
    print

if __name__ == "__main__":

    ts = [threading.Thread(target=crash_lps3, name='threading1') for i in range(100)]
    for t in ts:
        t.start()
    t.join()



