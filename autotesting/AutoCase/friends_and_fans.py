# -*- coding: utf-8 -*-
__author__ = 'Maiziedu'

from selenium import webdriver
import time
import math
import datetime
import login
from selenium.webdriver.common.keys import Keys
from mysql import update_output


def Search_fans(driver):
    username='qlp@qq.com'
    password='123123123'
    login.login_fps(username, password)
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[3]/div/ul/li[1]/a/span[1]').click()
    time.sleep(2)
    # 搜索好友
    driver.find_element_by_xpath('//*[@id="search-text"]/input').send_keys('S')
    time.sleep(3)
    driver.find_element_by_id('search-submit').click()
    time.sleep(3)
    if driver.find_elements_by_link_text('Sundy'):
        print('搜索成功')
        actual='Sundy'

    update_output('FPS_011','Sundy',actual)

Search_fans(login.driver)