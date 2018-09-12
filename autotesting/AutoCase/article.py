# _*_ coding:utf-8 _*_
__author__ = 'Administrator'

import requests
import sqls
import time
from pyquery import PyQuery as pq
from Autotesing import settings
from mysql import select
from public import equal, Driver, content_deal, time_deal


# 文章列表数据校验
class Article():
    def __init__(self):
        self.job_url = settings.SITE_URL + 'group/job'
        self.tech_url = settings.SITE_URL + 'group/tech'
        self.news_url = settings.SITE_URL + 'group/news'
        self.class_url = settings.SITE_URL + 'group/class'
        self.cafe_url = settings.SITE_URL + 'group/cafe'
        self.talk_url = settings.SITE_URL + 'group/talk'

    # 定义通用的文章列表数据
    def article_list(self, url):
        res = requests.get(url)
        txt = pq(res.text)
        item = txt('.article-list>.item')
        actual = list()
        for i in item:
            i = pq(i)
            img = i('.col-left>.col-in img').attr('src').split('uploads/')[-1]  # 文章题图
            link = i('.col-left>.col-in').attr('href')   # 文章链接，取出文章id
            title = i('.col-right>.col-in>h3').text()  # 文章标题
            content = i('.col-right>.col-in>p').text().replace('查看全文', '').replace(' ', '')[0:80] # 文章内容
            tags = i('.col-right>.col-in .hot-tag').text()  # 文章标签
            ava = i('.article-about-user img').attr('src').split('uploads/')[-1]  # 发表人头像
            nick_name = i('.article-about-user .u-name').text()  # 发布人昵称
            user_link = i('.article-about-user a').attr('href').split('/')[-1]  # 发布人动态链接
            date_publish = i('.u-datetime').text()  # 发布时间
            review_count = i('.icon-browse').text()  # 浏览数
            reply_count = i('.icon-ask').text()  # 回复数
            forward_count = i('.icon-good').text()  # 点赞数
            actual.append((img, link, title, content, tags, ava, nick_name,
                           user_link, date_publish, review_count, reply_count, forward_count))
        return actual

    # 通用处理artice_list的预期结果
    def article_list_expect(self, article_type):
        expect = select(sqls.article_list.replace('lilang_type', article_type))
        expect = list(expect)
        for i in range(len(expect)):
            expect[i] = list(expect[i])
            expect[i][2] = pq(content_deal(expect[i][2])).text()[0:49]
            expect[i][3] = pq(content_deal(expect[i][3])).text().replace(' ', '').replace(u'\xa0', '')[0:80]
            expect[i][4] = expect[i][4].replace(',', '') if expect[i][4] else ''
            expect[i][8] = time_deal(expect[i][8])
        return expect

    # 获取文章总数量
    def article_total_count(self, url):
        res = requests.get(url)
        txt = pq(res.text)
        item = txt('.zypage')
        if item.text() == '':
            total_count = len(txt('.article-list>.item'))
        else:
            page = pq(item)('#page-pane2').text()  # 总页数
            lp = pq(requests.get(url+'?page='+page).text)
            last_count = len(lp('.article-list>.item'))
            total_count = int(page)*10+last_count-10
        actual = list()
        actual.append((total_count,))
        return actual

    # 分页测试
    def article_page(self, url):
        res = requests.get(url)
        txt = pq(res.text)
        item = txt('.zypage')
        actual = list()
        if item.text() == '':
            actual.append(('1',))
        else:
            driver = Driver.driver_init()
            driver.get(url)
            driver.find_element_by_class_name('jp-last').click()
            time.sleep(2)
            last_page = driver.current_url.split('=')[-1]
            driver.find_element_by_class_name('jp-first').click()
            time.sleep(2)
            first_page = driver.current_url.split('=')[-1]
            driver.find_element_by_class_name('jp-next').click()
            time.sleep(2)
            next_page = driver.current_url.split('=')[-1]
            driver.find_element_by_class_name('jp-previous').click()
            time.sleep(2)
            pre_page = driver.current_url.split('=')[-1]
            driver.close()
            actual.append((last_page, first_page, next_page, pre_page))
        return actual

    # 文章热门标签
    def article_hot_tags(self, url):
        res = requests.get(url)
        txt = pq(res.text)
        item = txt('.hot-tag-box .hot-tag')
        actual = list()
        for i in item:
            i = pq(i)
            actual.append((i.text(),))  # 标签集合
        return actual

    # 文章版规
    def article_rule(self, url):
        res = requests.get(url)
        txt = pq(res.text)
        item = txt('.main-area-right .ibox-body>.notice-information')
        rule = pq(item).text()  # 规则集合
        actual = list()
        actual.append((rule,))
        return actual

    # 热门文章
    def article_hot_article(self, url):
        res = requests.get(url)
        txt = pq(res.text)
        item = txt('.hot-article-list>.item')
        actual = list()
        for i in item:
            i = pq(i)
            link = i('a').attr('href').split('/')[-1]  # 文章id
            title = i('a').text()  # 文章标题
            actual.append((link, title))
        return actual

    # 文章广告栏
    def article_ad(self, url):
        res = requests.get(url)
        txt = pq(res.text)
        item = txt('.bar-ad-pic>a')
        actual = list()
        for i in item:
            i = pq(i)
            link = i.attr('href')  # 广告链接
            img = i('img').attr('src')  # 广告链接
            actual.append((link, img))
        return actual

    # 未登录，发布文章
    def article_publish(self, url):
        driver = Driver.driver_init()
        driver.get(url)
        driver.find_element_by_xpath('/html/body/div[9]/div[5]/div/div/div[3]/div[1]/a').click()  # 点击发布
        time.sleep(3)
        txt = driver.find_element_by_id('login_btn').text  # 获取登录框上的元素，没得就洗了
        actual = list()
        actual.append((txt,))
        driver.close()
        return actual

    # 开始放大招了，用例执行开始，
    # 就业故事的list是否正确
    def job_list(self):
        actual = Article().article_list(self.job_url)
        expect = Article().article_list_expect('1')
        equal('job_list', expect, actual)

    # 技术文章的list是否正确
    def tech_list(self):
        actual = Article().article_list(self.tech_url)
        expect = Article().article_list_expect('2')
        equal('tech_list', expect, actual)

    # 麦子新闻的list是否正确
    def news_list(self):
        actual = Article().article_list(self.news_url)
        expect = Article().article_list_expect('3')
        equal('news_list', expect, actual)

    # 新课上线的list是否正确
    def class_list(self):
        actual = Article().article_list(self.class_url)
        expect = Article().article_list_expect('4')
        equal('class_list', expect, actual)

    # 麦聊吧的list是否正确
    def cafe_list(self):
        actual = Article().article_list(self.cafe_url)
        expect = Article().article_list_expect('6')
        equal('cafe_list', expect, actual)

    # 吐槽的list是否正确
    def talk_list(self):
        actual = Article().article_list(self.talk_url)
        expect = Article().article_list_expect('5')
        equal('talk_list', expect, actual)

    # 就业故事的总数量
    def job_total_count(self):
        actual = Article().article_total_count(self.job_url)
        expect = select(sqls.article_total_count.replace('lilang_type', '1'))
        equal('job_total_count', expect, actual)

    # 技术文章的总数量
    def tech_total_count(self):
        actual = Article().article_total_count(self.tech_url)
        expect = select(sqls.article_total_count.replace('lilang_type', '2'))
        equal('tech_total_count', expect, actual)

    # 麦子新闻的的总数量
    def news_total_count(self):
        actual = Article().article_total_count(self.news_url)
        expect = select(sqls.article_total_count.replace('lilang_type', '3'))
        equal('news_total_count', expect, actual)

    # 新课上线的总数量
    def class_total_count(self):
        actual = Article().article_total_count(self.class_url)
        expect = select(sqls.article_total_count.replace('lilang_type', '4'))
        equal('class_total_count', expect, actual)

    # 麦聊吧的总数量
    def cafe_total_count(self):
        actual = Article().article_total_count(self.cafe_url)
        expect = select(sqls.article_total_count.replace('lilang_type', '6'))
        equal('cafe_total_count', expect, actual)

    # 吐槽的list是否正确
    def talk_total_count(self):
        actual = Article().article_total_count(self.talk_url)
        expect = select(sqls.article_total_count.replace('lilang_type', '5'))
        equal('talk_total_count', expect, actual)

    # 就业故事的热门标签
    def job_hot_tags(self):
        actual = Article().article_hot_tags(self.job_url)
        expect = select(sqls.article_hot_tags)
        equal('job_hot_tags', expect, actual)

    # 技术文章的热门标签
    def tech_hot_tags(self):
        actual = Article().article_hot_tags(self.tech_url)
        expect = select(sqls.article_hot_tags)
        equal('tech_hot_tags', expect, actual)

    # 麦子新闻的热门标签
    def news_hot_tags(self):
        actual = Article().article_hot_tags(self.news_url)
        expect = select(sqls.article_hot_tags)
        equal('news_hot_tags', expect, actual)

    # 新课上线的热门标签
    def class_hot_tags(self):
        actual = Article().article_hot_tags(self.class_url)
        expect = select(sqls.article_hot_tags)
        equal('class_hot_tags', expect, actual)

    # 麦聊吧的热门标签
    def cafe_hot_tags(self):
        actual = Article().article_hot_tags(self.cafe_url)
        expect = select(sqls.article_hot_tags)
        equal('cafe_hot_tags', expect, actual)

    # 吐槽的热门标签
    def talk_hot_tags(self):
        actual = Article().article_hot_tags(self.talk_url)
        expect = select(sqls.article_hot_tags)
        equal('talk_hot_tags', expect, actual)

    # 就业故事的版规
    def job_rule(self):
        actual = Article().article_rule(self.job_url)
        expect = list()
        expect.append((sqls.article_rule,))
        equal('job_rule', expect, actual)

    # 技术文章的版规
    def tech_rule(self):
        actual = Article().article_rule(self.tech_url)
        expect = list()
        expect.append((sqls.article_rule,))
        equal('tech_rule', expect, actual)

    # 麦子新闻的版规
    def news_rule(self):
        actual = Article().article_rule(self.news_url)
        expect = list()
        expect.append((sqls.article_rule,))
        equal('news_rule', expect, actual)

    # 新课上线的版规
    def class_rule(self):
        actual = Article().article_rule(self.class_url)
        expect = list()
        expect.append((sqls.article_rule,))
        equal('class_rule', expect, actual)

    # 麦聊吧的版规
    def cafe_rule(self):
        actual = Article().article_rule(self.cafe_url)
        expect = list()
        expect.append((sqls.article_rule,))
        equal('cafe_rule', expect, actual)

    # 吐槽的版规
    def talk_rule(self):
        actual = Article().article_rule(self.talk_url)
        expect = list()
        expect.append((sqls.article_rule,))
        equal('talk_rule', expect, actual)

    # 就业故事的热门文章
    def job_hot_job(self):
        actual = Article().article_hot_article(self.job_url)
        expect = select(sqls.article_hot_article)
        equal('job_hot_job', expect, actual)

    # 技术文章的热门文章
    def tech_hot_tech(self):
        actual = Article().article_hot_article(self.tech_url)
        expect = select(sqls.article_hot_article)
        equal('tech_hot_tech', expect, actual)

    # 麦子新闻的热门文章
    def news_hot_news(self):
        actual = Article().article_hot_article(self.news_url)
        expect = select(sqls.article_hot_article)
        equal('news_hot_news', expect, actual)

    # 新课上线的热门文章
    def class_hot_class(self):
        actual = Article().article_hot_article(self.class_url)
        expect = select(sqls.article_hot_article)
        equal('class_hot_class', expect, actual)

    # 麦聊吧的热门文章
    def cafe_hot_cafe(self):
        actual = Article().article_hot_article(self.cafe_url)
        expect = select(sqls.article_hot_article)
        equal('cafe_hot_cafe', expect, actual)

    # 吐槽的热门文章
    def talk_hot_talk(self):
        actual = Article().article_hot_article(self.talk_url)
        expect = select(sqls.article_hot_article)
        equal('talk_hot_talk', expect, actual)

    # # 就业故事的广告,先按兵不动，正式网站根本没使用此功能
    # def job_ad(self):
    #     actual = Article().article_ad(self.talk_url)
    #     expect = select(sqls.article_hot_article)
    #     equal('talk_hot_talk', expect, actual)

    # 就业故事的登录
    def job_publish(self):
        actual = Article().article_publish(self.job_url)
        expect = list()
        expect.append(('登录', ))
        equal('job_publish', expect, actual)

    # 技术文章的登录
    def tech_publish(self):
        actual = Article().article_publish(self.tech_url)
        expect = list()
        expect.append(('登录', ))
        equal('tech_publish', expect, actual)

    # 麦子新闻的登录
    def news_publish(self):
        actual = Article().article_publish(self.news_url)
        expect = list()
        expect.append(('登录', ))
        equal('news_publish', expect, actual)

    # 新课上线的登录
    def class_publish(self):
        actual = Article().article_publish(self.class_url)
        expect = list()
        expect.append(('登录', ))
        equal('class_publish', expect, actual)

    # 麦聊吧的登录
    def cafe_publish(self):
        actual = Article().article_publish(self.cafe_url)
        expect = list()
        expect.append(('登录', ))
        equal('cafe_publish', expect, actual)

    # 吐槽的登录
    def talk_publish(self):
        actual = Article().article_publish(self.talk_url)
        expect = list()
        expect.append(('登录', ))
        equal('talk_publish', expect, actual)

    # 就业故事的分页
    def job_page(self):
        actual = Article().article_page(self.job_url)
        total = select(sqls.article_total_count.replace('lilang_type', '1'))
        if total[0][0] % 10 > 0:
            count = total[0][0]/10+1
        else:
            count = total[0][0]/10
        expect = list()
        if count > 1:
            expect.append((count, '1', '2', '1'))
        else:
            expect.append(('1',))
        equal('job_page', expect, actual)

    # 技术文章的分页
    def tech_page(self):
        actual = Article().article_page(self.tech_url)
        total = select(sqls.article_total_count.replace('lilang_type', '2'))
        if total[0][0] % 10 > 0:
            count = total[0][0]/10+1
        else:
            count = total[0][0]/10
        expect = list()
        if count > 1:
            expect.append((count, '1', '2', '1'))
        else:
            expect.append(('1',))
        equal('tech_page', expect, actual)

    # 麦子新闻的分页
    def news_page(self):
        actual = Article().article_page(self.news_url)
        total = select(sqls.article_total_count.replace('lilang_type', '3'))
        if total[0][0] % 10 > 0:
            count = total[0][0]/10+1
        else:
            count = total[0][0]/10
        expect = list()
        if count > 1:
            expect.append((count, '1', '2', '1'))
        else:
            expect.append(('1',))
        equal('news_page', expect, actual)

    # 新课上线的分页
    def class_page(self):
        actual = Article().article_page(self.class_url)
        total = select(sqls.article_total_count.replace('lilang_type', '4'))
        if total[0][0] % 10 > 0:
            count = total[0][0]/10+1
        else:
            count = total[0][0]/10
        expect = list()
        if count > 1:
            expect.append((count, '1', '2', '1'))
        else:
            expect.append(('1',))
        equal('class_page', expect, actual)

    # 麦聊吧的分页
    def cafe_page(self):
        actual = Article().article_page(self.cafe_url)
        total = select(sqls.article_total_count.replace('lilang_type', '6'))
        if total[0][0] % 10 > 0:
            count = total[0][0]/10+1
        else:
            count = total[0][0]/10
        expect = list()
        if count > 1:
            expect.append((count, '1', '2', '1'))
        else:
            expect.append(('1',))
        equal('cafe_page', expect, actual)

    # 吐槽的分页
    def talk_page(self):
        actual = Article().article_page(self.talk_url)
        total = select(sqls.article_total_count.replace('lilang_type', '5'))
        if total[0][0] % 10 > 0:
            count = total[0][0]/10+1
        else:
            count = total[0][0]/10
        expect = list()
        if count > 1:
            expect.append((count, '1', '2', '1'))
        else:
            expect.append(('1',))
        equal('talk_page', expect, actual)

if __name__ == '__main__':
    Article().job_page()

    Article().tech_page()
    Article().news_page()
    Article().class_page()
    Article().cafe_page()
    Article().talk_page()










