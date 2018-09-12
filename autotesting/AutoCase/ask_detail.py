# _*_ coding:utf-8 _*_
__author__ = 'Administrator'

import requests
import sqls
import time
from Autotesing import settings
from pyquery import PyQuery as pq
from pymysql import select
from public import equal, Driver, login_lps, content_deal, time_deal

# 学习问答列表数据展示

# 使用selenium 来搞数据
class AskDetail():
    def __init__(self, ask_id):
        self.ask_id = ask_id
        ask_url = settings.SITE_URL+"group/ask/"+self.ask_id
        if pq(requests.get(ask_url).content)('title').text() == '404错误 - 麦子学院':
            base_url = settings.SITE_URL+"group/course_ask/"+self.ask_id
        else:
            base_url = ask_url
        self.driver = Driver.driver_init()
        self.driver.get(base_url)
        time.sleep(2)
        resp = requests.get(base_url)
        self.txt = pq(resp.text)

    # 获取课程问答详情等数据
    def ask_detail_base_info(self):
        driver = self.driver
        actual = list()
        main = driver.find_element_by_class_name('QA-text-box')  # 获取详情主体框
        title = main.find_element_by_tag_name('h1').text  # 问答标题
        content = main.find_element_by_class_name('QA-text-main').text  # 问答内容
        tags = main.find_element_by_class_name('hot-tag-group').text  # 问答标签
        nick_name = main.find_element_by_class_name('u-name').text  # 发布人昵称
        publish_date = main.find_element_by_class_name('u-datetime').text  # 发布日期
        forward_count = main.find_element_by_class_name('praise-btn').text.split()[-1]  # 点赞数
        collect_count = main.find_element_by_class_name('u-collect').text.split()[-1]  # 收藏数
        review_count = main.find_element_by_class_name('u-view').text.split()[-1]  # 浏览数
        time.sleep(3)
        driver.close()
        actual.append((title, content, tags, nick_name, publish_date, forward_count, collect_count, review_count))
        expect = select(sqls.ask_detail_base_info.replace('lilang_id', self.ask_id))
        expect = list(expect)
        for i in range(len(expect)):
            expect[i] = list(expect[i])
            expect[i][1] = pq(content_deal(expect[i][1])).text()
            expect[i][2] = expect[i][2].replace(',', ' ')
            expect[i][4] = time_deal(expect[i][4])
            expect[i][7] -= 1
        equal('ask_detail_base_info', expect, actual)

    # 获取开放问答详情
    def ask_detail_course_ask_base_info(self):
        driver = self.driver
        actual = list()
        main = driver.find_element_by_class_name('QA-text-box')  # 获取详情主体框
        title = main.find_element_by_tag_name('h1').text  # 问答标题
        content = main.find_element_by_class_name('QA-text-main').text.replace('\n', '').replace(' ', '')  # 问答内容
        tags = main.find_element_by_class_name('hot-tag-group').text  # 问答标签
        source = main.find_element_by_class_name('art_zy_edit').text.split('源自：')[-1]  # 源自
        nick_name = main.find_element_by_class_name('u-name').text  # 发布人昵称
        publish_date = main.find_element_by_class_name('u-datetime').text  # 发布日期
        forward_count = main.find_element_by_xpath('/html/body/div[9]/div[5]/div/div/div[1]/div/'
                                                   'div[1]/div[3]/div[2]/span[2]').text  # 点赞数
        collect_count = main.find_element_by_class_name('u-collect').text.split()[-1]  # 收藏数
        review_count = main.find_element_by_class_name('u-view').text.split()[-1]  # 浏览数
        time.sleep(3)
        driver.close()
        actual.append((title, content, tags, source, nick_name, publish_date, forward_count, collect_count, review_count))
        expect = select(sqls.ask_detail_course_ask_base_info.replace('lilang_id', self.ask_id))
        expect = list(expect)
        for i in range(len(expect)):
            expect[i] = list(expect[i])
            expect[i][1] = pq(content_deal(expect[i][1])).text().replace(' ', '')
            expect[i][5] = time_deal(expect[i][5])
            expect[i][8] -= 1
        equal('ask_detail_course_ask_base_info', expect, actual)

    # 获取问答第一页的评论数据，我擦擦啊
    def ask_detail_discuss(self):
        driver = self.driver
        item = driver.find_element_by_id('comments').find_elements_by_class_name('item')
        time.sleep(3)
        actual = list()
        for i in item:
            if i.text != '':  # 这里标签有重复，去除哪些没得内容的，不要坑我
                ava = i.find_element_by_tag_name('a').get_attribute('href').split('dynmsg/')[-1]  # 动态链接
                nick_name = i.find_element_by_class_name('u-name').text  # 昵称
                date_publish = i.find_element_by_class_name('u-datetime').text  # 发布日期
                content = i.find_element_by_class_name('zy_shou11').text.replace(' ', '')  # 发布内容
                count = i.find_element_by_class_name('icon-label-text').text  # 点赞数
                actual.append((ava, nick_name, date_publish, content, count))
        driver.close()
        expect = select(sqls.ask_discuss.replace('lilang_id', self.ask_id))
        expect = list(expect)
        for i in range(len(expect)):
            expect[i] = list(expect[i])
            expect[i][2] = time_deal(expect[i][2])
            expect[i][3] = pq(content_deal(expect[i][3])).text().replace(' ', '')
        actual = actual if actual else ['null']
        expect = expect if expect else ['null']
        equal('ask_detail_discuss', expect, actual)

    # 问答详情热门标签
    def ask_detail_hot_tags(self):
        driver = self.driver
        item = driver.find_element_by_class_name('hot-tag-boxin').find_elements_by_class_name('hot-tag')
        actual = list()
        for i in item:
            tag = i.text
            actual.append((tag,))
        expect = select(sqls.ask_hot_tags)
        equal('ask_detail_hot_tags', expect, actual)
        driver.close()

    # 获取开放问答的相关问答
    def ask_detail_relate_ask(self):
        actual = list()
        item = self.txt('.hot-QA-list>.item')
        for i in item:
            i = pq(i)
            link = i('a').attr('href').split('/')[-1]  # 问答链接
            count = i('a>span').text().split()[0]  # 回答数量
            title = i('a').remove('span').text()  # 问答标题
            actual.append((link, title, count))
        actual = actual if actual else ['无相关问答']
        expect = select(sqls.ask_detail_relate_ask.replace('lilang_id', self.ask_id))
        expect = expect if expect else ['无相关问答']
        equal('ask_detail_relate_ask', expect, actual)
        self.driver.close()

    # 获取课程问答的相关问答,代码有部分重复,需要传入课程问答id
    def ask_detail_relate_course_ask(self):
        actual = list()
        item = self.txt('.hot-QA-list>.item')
        for i in item:
            i = pq(i)
            link = i('a').attr('href').split('/')[-1]  # 问答链接
            count = i('a>span').text().split()[0]  # 回答数量
            title = i('a').remove('span').text()  # 问答标题
            actual.append((link, title, count))
        actual = actual if actual else ['无相关问答']
        expect = select(sqls.ask_detail_relate_course_ask.replace('lilang_id', self.ask_id))
        expect = expect if expect else ['无相关问答']
        equal('ask_detail_relate_course_ask', expect, actual)


if __name__ == "__main__":
    AskDetail('12541').ask_detail_discuss()
    print 'test'
