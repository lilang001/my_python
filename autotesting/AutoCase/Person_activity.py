# -*- coding: utf-8 -*-
__author__ = 'Maiziedu'

from selenium import webdriver
import time
import math
import datetime
import login
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from connectDB import update_output,select
from html_tag import filter_html_tag

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


username='qlp@qq.com'
password='123123123'

def My_article(driver,content):
    login.login_fps(username,password)
    time.sleep(5)
    # 点击动态
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/ul/li[2]/a/span').click()
    time.sleep(10)
    # 点击我的活动
    driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div/div[2]/ul/li[3]/a/span[1]').click()
    print('成功')
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="MY_ACTIVITY"]/div/div[1]/div[2]/div/h3/a').click()
    driver.find_elements_by_link_text(u'活动详情')
    a=driver.find_elements_by_link_text(u'活动详情')

    if a==driver.find_elements_by_link_text(u'活动详情'):
        actual='进入活动详情页'
        print('find')
        update_output('FPS_004', '进入活动详情页',actual)
    # 评论问答
    time.sleep(10)

    driver.switch_to_window(driver.window_handles[1])
    # driver.refresh()
    # 滑动滚动条到评论窗口
    js="document.body.scrollTop=2000;"
    driver.execute_script(js)
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
    update_output('FPS_011',content,actual)



My_article(login.driver,U'漆来平猪猪猪')


# if __name__ == '__main__':
#     actual = select('select content from mz_forum_discuss  where user=2218 order BY date_publish  DESC limit 0,1 ;')
#     actual = filter_html_tag(str(actual[0][0]))
#     content = '猪猪猪'
#     update_output('FPS_011', content, actual)