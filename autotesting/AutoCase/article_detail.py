# _*_ coding:utf-8 _*_
__author__ = 'Administrator'

import requests
import sqls
import time
from pyquery import PyQuery as pq
from Autotesing import settings
from mysql import select
from public import equal, Driver, content_deal, time_deal

class ArticleDetail():
    def __init__(self, article_id):
        self.article_id = article_id
        self.url = settings.SITE_URL + 'group/article/' + self.article_id
        print self.url
        self.res = requests.get(self.url)
        self.txt = self.res.text

    # 文章详细的基础内容
    def article_detail_info(self):
        item = pq(self.txt)('.article-text-box')
        title = item('h1').text()  # 文章标题
        ava_img = item('img').attr('src').split('uploads/')[-1]  # 发布人头像图片
        ava_link = item('.u-photo-btn').attr('href').split('/')[-1]  # 发布人动态链接
        nick_name = item('.u-name').text()  # 发布人昵称
        date_publish = item('.u-datetime').text()  # 发布时间
        tags = item('.hot-tag-group').text()  # 文章标签
        content = item('#article').text().replace('\n', '').replace(' ', '')  # 文章内容
        forward_count = item('.col-right span').eq(2).text()  # 点赞数
        collect_count = item('.col-right #whole_article').text().split()[-1]  # 收藏数
        review_count = item('.col-right .u-view').text().split()[-1]  # 浏览数
        actual = list()
        actual.append((title, ava_img, ava_link, nick_name, date_publish, tags, content, forward_count, collect_count, review_count))
        expect = select(sqls.articel_detail_info.replace('lilang_type', self.article_id))
        expect = list(expect)
        for i in range(len(expect)):
            expect[i] = list(expect[i])
            expect[i][5] = expect[i][5].replace(',', '') if expect[i][5] else ''
            expect[i][6] = pq(content_deal(expect[i][6])).text().replace(' ', '')
        equal('article_detail_info', expect, actual)

    # 文章详情的评论内容
    def article_detail_discuss(self):
        driver = Driver.driver_init()
        driver.get(self.url)
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
        expect = select(sqls.ask_discuss.replace('lilang_id', self.article_id))  # 用问答的sql可以一样的玩
        expect = list(expect)
        for i in range(len(expect)):
            expect[i] = list(expect[i])
            expect[i][2] = time_deal(expect[i][2])
            expect[i][3] = pq(content_deal(expect[i][3])).text().replace(' ', '')
        actual = actual if actual else ['null']
        expect = expect if expect else ['null']
        equal('article_detail_discuss', expect, actual)

    # 文章的热门标签
    def article_detail_tags(self):
        item = pq(self.txt)('.hot-tag-box .hot-tag')
        actual = list()
        for i in item:
            i = pq(i)
            actual.append((i.text(),))  # 标签集合
        expect = select(sqls.article_hot_tags)
        equal('article_detail_tags', expect, actual)

    # 相关文章，通过标签来找的
    def article_detail_relate(self):
        item = pq(self.txt)('.hot-article-list>.item')
        actual = list()
        for i in item:
            i = pq(i)
            link = i('a').attr('href').split('/')[-1]  # 链接
            title = i.text()  # 标题
            actual.append((link, title))
        actual = actual if actual else ['无相关问答']
        expect = select(sqls.article_detail_relate.replace('lilang_id', self.article_id))
        expect = expect if expect else ['无相关问答']
        equal('article_detail_relate', expect, actual)

    # 作者的其他文章
    def article_detail_other(self):
        item = pq(self.txt)('#authorElseArticle .hot-article-list .item')
        actual = list()
        for i in item:
            i = pq(i)
            link = i('a').attr('href').split('/')[-1]  # 链接
            title = i.text()  # 标题
            actual.append((link, title))
        actual = actual if actual else ['无相关问答']
        expect = select(sqls.article_detail_relate.replace('lilang_id', self.article_id))
        expect = expect if expect else ['无相关问答']
        equal('article_detail_other', expect, actual)










if __name__ == "__main__":
    # ArticleDetail('10773').article_detail_info()
    # ArticleDetail('10773').article_detail_discuss()
    # ArticleDetail('10773').article_detail_tags()
    # ArticleDetail('10773').article_detail_relate()
    ArticleDetail('10773').article_detail_other()

