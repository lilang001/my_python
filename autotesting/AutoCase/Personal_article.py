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

def enter_publish_article(driver):
    login.login_fps(username,password)
    time.sleep(8)
    # 点击动态
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/ul/li[2]/a/span').click()
    time.sleep(10)
    # 点击我的文章
    driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div/div[2]/ul/li[2]/a/span[1]').click()
    print('成功')
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="WZ"]/div/div/div[1]/a').click()
    time.sleep(5)
    print('test')
    if driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/div/div[1]/span'):

        actual='进入发布文章页面'

    print(actual)

    update_output('FPS_009','进入发布文章页面',actual)
    time.sleep(3)

def My_article(driver,content):
    login.login_fps(username,password)
    time.sleep(8)
    # 点击动态
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/ul/li[2]/a/span').click()
    time.sleep(10)
    # 点击我的文章
    driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div/div[2]/ul/li[2]/a/span[1]').click()
    print('成功')
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="MY_ARTICLE"]/div[1]/div[1]/div[2]/div/h3/a').click()
    driver.find_elements_by_link_text(u'文章详情')
    a=driver.find_elements_by_link_text(u'文章详情')

    if a==driver.find_elements_by_link_text(u'文章详情'):
        actual='进入文章详情页'
        print('find')
        update_output('FPS_004','进入文章详情页',actual)
    # 评论问答
    time.sleep(10)
    driver.refresh()
    driver.switch_to_window(driver.window_handles[1])
    driver.switch_to_frame("ueditor_0")
    driver.find_element_by_xpath("/html/body").send_keys(content)
    time.sleep(3)
    driver.switch_to.default_content()
    print('pass')
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="main-reply"]').click()
    print('评论成功')
    actual=select('select content from mz_forum_discuss  where user=2218 order BY date_publish  DESC limit 0,1 ;')
    actual=filter_html_tag(str(actual[0][0]))
    print(actual[0][0])
    update_output('FPS_010',content,actual)



def publish_article(driver):
    driver.find_element_by_id("id_title").send_keys('tttttttttttttttttttttttttttttttttttttttt')
    time.sleep(5)

    driver.find_element_by_xpath('//*[@id="select_aritcle_image"]/a').click()
    time.sleep(3)
    driver.find_element_by_id("file_upload").send_keys("E:\\Pictures\\lyp.jpg")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="upload-pane"]/div[2]/button').click()
    driver.switch_to_frame("ueditor_0")
    driver.find_element_by_xpath("/html/body").send_keys(u'猪猪猪猪猪猪猪猪猪猪猪猪猪猪猪猪猪猪猪猪猪猪猪猪猪')
    driver.switch_to.default_content()
    driver.find_element_by_id("inpTags").send_keys('php')
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[13]/div/div/a').click()
    driver.find_element_by_id("inpTags").click()
    # ActionChains(driver).move_to_element(u'文章类型')
    time.sleep(3)
    driver.find_element_by_id("post_art_1").click()

    print('文章发布成功')



def Article_Collection(driver):
    login.login_fps(username,password)
    time.sleep(8)
    # 点击动态
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/ul/li[2]/a/span').click()
    time.sleep(10)
    # 点击我的文章
    driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div/div[2]/ul/li[2]/a/span[1]').click()
    time.sleep(8)
    print('成功')
    # 点击我的收藏
    driver.find_element_by_xpath('//*[@id="WZ"]/div/div/div[1]/ul/li[2]/a[2]')
    if driver.find_element_by_link_text(u'要不要来讨论一下评论和文章该换哪种富文本编辑器呢'):
        content='要不要来讨论一下评论和文章该换哪种富文本编辑器呢'

    actual=select('SELECT mz_forum_entity.title from mz_forum_entity , mz_forum_article where mz_forum_entity.id=mz_forum_article.entity_ptr_id and mz_forum_entity.user=2218 ORDER BY mz_forum_entity.date_publish DESC limit 0,1 ;')
    actual=filter_html_tag(str(actual[0][0]))
    update_output('FPS_007',content,actual)



# enter_publish_article(login.driver)
# My_article(login.driver,u'测试测试测试')
# publish_article(login.driver)
Article_Collection(login.driver)