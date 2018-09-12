# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from selenium import webdriver
import time
import math
import datetime
from selenium.webdriver.common.keys import Keys

# webdriver实例,初始化一个浏览器窗口
driver = webdriver.Chrome()
#定义一个访问地址
username='qlp@qq.com'
password='123123123'
# 登录
def login_fps(username, password):

    base_url = "http://192.168.1.142/group/"
    driver.get(base_url)
    driver.maximize_window()
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="searchTip"]/div/i').click()
    ele=driver.find_element_by_link_text('登录').click()
    # a = driver.switch_to_alert()
    time.sleep(3)
    driver.find_element_by_id("id_account_l").send_keys(username)
    driver.find_element_by_id("id_password_l").send_keys(password)
    driver.find_element_by_id("login_btn").click()
    time.sleep(10)
    print("登录成功")













