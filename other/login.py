# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from selenium import webdriver
import time
import math
import datetime
from mysql import result, update_output, fps_conn
from selenium.webdriver.common.keys import Keys

# webdriver实例,初始化一个浏览器窗口
driver = webdriver.Firefox()
#定义一个访问地址
base_url = "http://192.168.1.142/group/ask"
# 登录
def login_fps(username, password):
    driver.get(base_url)
    driver.maximize_window()
    driver.find_element_by_xpath("//*[@id=\"microoh-navbar-collapse\"]/div[1]/div/a[1]").click()
    a = driver.switch_to_alert()
    time.sleep(3)
    driver.find_element_by_id("id_account_l").send_keys(username)
    driver.find_element_by_id("id_password_l").send_keys(password)
    driver.find_element_by_id("login_btn").click()
    time.sleep(4)


# 登录校验
def login():
    login_fps('qlp@qq.com','123123123')
    # 获取登录后用户昵称
    nickname = driver.find_element_by_xpath('/html/body/div[3]/header/div/div[2]/div[1]/div[1]/dl/dt/a[2]/span').text
    # 更新数据库中实际获取到的用户昵称
    update_output(nickname, 1)
    # 校验期望与实际是否一致
    result(1)


# 发布问答,只有标题和内容
def publish_ask(tile, content):
    # 先跳转到问答首页
    driver.get("http://192.168.1.142/group/ask")
    time.sleep(3)
    driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div[2]/a").click()
    driver.find_element_by_id("form-title").send_keys(tile)
    driver.switch_to_frame("ueditor_0")
    driver.find_element_by_xpath("/html/body").send_keys(content)
    driver.switch_to.default_content()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[2]/form/div[5]/div/button").click()



# 发布文章

def publish_article(tile, content):
    # 跳转文章页面
    time.sleep(3)
    driver.get("http://192.168.1.142/group/article")
    time.sleep(3)
    # 点击发布文章按钮
    driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div[2]/a").click()
    # 输入文章内容
    driver.find_element_by_id("id_title").send_keys(tile)
    driver.switch_to_frame("ueditor_0")
    driver.find_element_by_xpath("/html/body").send_keys(content)
    driver.switch_to.default_content()
    time.sleep(1)
    # 选择文章图片
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[2]/form/div[3]/div/a").click()
    time.sleep(1)
    driver.find_element_by_id("file_upload").send_keys("D:\\Pictures\\1231211321lilang.jpg")
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div/div[2]/div/div[2]/button").click()
    time.sleep(1)
    # 点击发布按钮
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[2]/form/div[7]/div/button").click()
    # 校验该用户最新的文章是否和刚才发布的一致
    conn2 = fps_conn().cursor()
    conn2.execute('select title,content,date_publish from mz_forum_entity where user=2218  order by date_publish desc limit 1')
    out_put = conn2.fetchall()
    update_output(out_put[0][0]+out_put[0][1]+out_put[0][2], 2)
    result(2)

# 当前时间相差小于3分钟
# def compare_datetime( s):
#     datetime date_publish1
#     s = datetime.datetime.now()
#     if s-date_publish1

login_fps('qlp@qq.com', '123123123')
publish_article('title', 'content')


# update_output(out_put[],out_put)