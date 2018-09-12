# -*- coding: utf-8 -*-
__author__ = 'Administrator'

import requests
import sqls
import time
from Autotesing import settings
from pyquery import PyQuery as pq
from mysql import select
from public import equal, Driver, content_deal, time_deal

# 学习问答列表数据展示
class Ask():
    def __init__(self):
        self.url = settings.SITE_URL+"group/ask"
        resp = requests.get(self.url)
        self.txt = pq(resp.text)
        self.driver = Driver.driver_init()
        self.driver.get(self.url)
        time.sleep(2)

    def ask_list(self):
        item = self.txt('.QA-list>.item')
        actual = list()
        for i in item:
            i = pq(i)
            ava = i('.col-left').find('img').attr('src').split('uploads/')[-1]# 头像地址
            nick_name = i('.u-name').text()  # 昵称
            title = i('.col-right h3>a').text()  # 问答标题
            reply = i('.item-r-A').text().split('[最新回答]')[-1].replace(' 查看详细', '')[0:100]  # 最新回复
            tags = i('.hot-tag-group .hot-tag').text()  # 问答标签
            tags = tags if tags else None
            source = i('.hot-tag-group .from-where').text().split('源自： ')[-1]  # 源自xx
            date_publish = i('.datetime').text()  # 发布时间
            review_count = i('.icon-browse').text()  # 浏览数
            reply_count = i('.icon-ask').text()  # 回复数
            forward_count = i('.icon-good').text()  # 点赞数
            actual.append((ava, nick_name, title, reply, tags, source, date_publish, review_count, reply_count, forward_count))
        self.driver.close()
        expect = select(sqls.ask_list)
        expect = list(expect)
        for i in range(len(expect)):
            expect[i] = list(expect[i])
            expect[i][2] = pq(content_deal(expect[i][2])).text()[0:49]
            print i, expect[i][3]
            expect[i][3] = expect[i][3] if expect[i][3] else u'还没有人回答这个问题呢...'
            expect[i][3] = pq(content_deal(expect[i][3])).text()[0:100]
            expect[i][4] = expect[i][4].replace(',', '') if expect[i][4] else expect[i][4]
            expect[i][6] = time_deal(expect[i][6])

        equal('ask_list', expect, actual)

    # 问答总条数
    def ask_total_count(self):
        item = self.txt('.zypage')
        page = pq(item)('#page-pane2').text()  # 总页数
        lp = pq(requests.get(self.url+'?page='+page).text)
        last_count = len(lp('.QA-list>.item'))
        total_count = int(page)*20+last_count-20
        actual = list()
        actual.append((total_count,))
        expect = select(sqls.ask_count)
        equal('ask_total_count', expect, actual)

    # 问答热门标签
    def ask_hot_tags(self):
        item = self.txt('.hot-tag-box .hot-tag')
        actual = list()
        for i in item:
            i = pq(i)
            actual.append((i.text(),))  # 标签集合
        expect = select(sqls.ask_hot_tags)
        equal('ask_hot_tags', expect, actual)

    # 问答版规
    def ask_rule(self):
        item = self.txt('.main-area-right .ibox-body>.notice-information')
        rule = pq(item).text()  # 规则集合
        actual = list()
        actual.append((rule,))
        expect = list()
        expect.append((sqls.ask_rule,))
        equal('ask_rule', expect, actual)

    # 热门问答排行榜
    def ask_hot_qa(self):
        item = self.txt('#hotQA .item')
        actual = list()
        for i in item:
            i = pq(i)
            link = i('a').attr('href').split('/')[-1]  # 问答链接
            count = i('a>span').text().split()[0]  # 回答数量
            title = i('a').remove('span').text()  # 问答标题
            actual.append((link, title, count))
        self.driver.close()
        expect = select(sqls.ask_hot_qa)
        equal('ask_hot_qa', expect, actual)

    def ask_publish(self):
        driver = self.driver
        driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div[2]/div[1]/a').click()
        time.sleep(4)
        actual = list()
        txt = driver.find_element_by_class_name('good-tips').find_element_by_tag_name('a').text
        actual.append((txt,))
        driver.close()
        expect = list()
        expect.append(('忘记密码？',))
        equal('ask_publish', expect, actual)

    def ask_rank(self):
        driver = self.driver
        lists = driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div[2]/div[6]')
        item = lists.find_elements_by_tag_name('li')
        actual = list()
        for i in item:
            link = i.find_element_by_tag_name('a').get_attribute('href').split('/')[-1]  # 用户链接
            ava = i.find_element_by_tag_name('img').get_attribute('src').split('http://192.168.1.142//uploads/')[-1]
            nick_name = i.find_element_by_class_name('a1').text  # 昵称
            desc = i.find_element_by_class_name('a2').text  # 用户介绍
            count = i.find_element_by_class_name('huoBox_ul_font2').text.split()[0]  # 回答数量
            actual.append((link, ava, nick_name, desc, count))
        driver.close()
        expect = select(sqls.ask_rank)
        expect = expect if expect else ['无数据']
        equal('ask_rank', expect, actual)

if __name__ == "__main__":
    Ask().ask_hot_tags()
    Ask().ask_hot_qa()
    Ask().ask_list()
    Ask().ask_publish()
    Ask().ask_rank()
    Ask().ask_rule()
    Ask().ask_total_count()

