# -*- coding: utf-8 -*-
__author__ = 'Maiziedu'

from selenium import webdriver
import time
import re
import datetime

import login
from selenium.webdriver.common.keys import Keys
from connectDB import update_output,select
from html_tag import filter_html_tag
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def enter_publish_ask(driver):

    login.login_fps(login.username,login.password)
    time.sleep(10)
    print('成功')
    # 点击动态
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/ul/li[2]/a/span').click()
    time.sleep(10)
    # 点击我的问答
    driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div/div[2]/ul/li[1]/a/span[1]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="WD"]/div/div/div[1]/a').click()
    time.sleep(5)
    print('test')
    if driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/div/div[1]/span'):

        actual='进入发布问答页面'

    print(actual)

    update_output('FPS_004','进入发布问答页面',actual)



def My_ask(driver,content):

    login.login_fps(login.username,login.password)
    time.sleep(10)
    print('成功')
    # 点击动态
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/ul/li[2]/a/span').click()
    time.sleep(10)
    # 点击我的问答
    driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div/div[2]/ul/li[1]/a/span[1]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="MY_QA"]/div[1]/div[1]/div[2]/div/h3/a').click()
    time.sleep(3)

    driver.find_elements_by_link_text(u'问答详情')
    a=driver.find_elements_by_link_text(u'问答详情')

    if a==driver.find_elements_by_link_text(u'问答详情'):
        actual='进入问答详情页'
        print('find')
        update_output('FPS_005','进入问答详情页',actual)

    time.sleep(3)
    driver.switch_to_window(driver.window_handles[1])
    # driver.refresh()
    # 滑动滚动条到评论窗口
    # js="document.body.scrollTop=2000;"
    # driver.execute_script(js)
    time.sleep(6)
    driver.switch_to_frame("ueditor_0")
    driver.find_element_by_xpath("/html/body").send_keys(content)

    time.sleep(3)
    driver.switch_to.default_content()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="main-reply"]').click()
    time.sleep(3)
    actual=select('select content from mz_forum_discuss  where user=2218 order BY date_publish  DESC limit 0,1 ;')
    time.sleep(3)
    actual=filter_html_tag(str(actual[0][0]))
    print(actual[0][0])

    update_output('FPS_006',content,actual)




def publish_ask(driver,title,content):
    driver.find_element_by_id("form-title").send_keys(title)
    time.sleep(3)
    driver.switch_to_frame("ueditor_0")
    driver.find_element_by_xpath("/html/body").send_keys(content)
    driver.switch_to.default_content()
    driver.find_element_by_id("inpTags").send_keys('java')
    print("走错了")
    driver.find_element_by_xpath("/html/body/div[8]/div/div/a[1]").click()
    time.sleep(3)
    driver.find_element_by_id("post_ask_1").click()
    print('发布问答成功')


def Ask_Collection(driver):
    login.login_fps(login.username,login.password)
    time.sleep(10)
    print('成功')
    # 点击动态
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/ul/li[2]/a/span').click()
    time.sleep(10)
    # 点击我的问答
    driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div/div[2]/ul/li[1]/a/span[1]').click()
    time.sleep(3)
    # 点击我的收藏
    driver.find_element_by_xpath('//*[@id="WD"]/div/div/div[1]/ul/li[3]/a/span')
    if driver.find_element_by_link_text(u'积极健康'):
        content='积极健康'

    actual=select('SELECT mz_forum_entity.title from mz_forum_entity , mz_forum_discuss where mz_forum_entity.id=mz_forum_discuss.relate_id and mz_forum_entity.`user`=2218 ORDER BY mz_forum_entity.date_publish DESC limit 0,1 ;')
    actual=filter_html_tag(str(actual[0][0]))
    update_output('FPS_003',content,actual)



    time.sleep(3)


# Ask_Collection(login.driver)
My_ask(login.driver,u'猪猪猪猪猪猪')
# enter_publish_ask(login.driver)
