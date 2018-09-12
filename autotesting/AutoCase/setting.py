#-*- coding: utf-8 -*-

__author__ = 'Maiziedu'
from selenium import webdriver
import time
import math
import datetime
import login
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from mysql import update_output,select



def setting(driver):
    username='qlp@qq.com'
    password='123123123'
    login.login_fps(username, password)
    time.sleep(5)
    driver.find_element_by_link_text('个人设置').click()
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="user_info_save"]/div[1]/div/span[3]/a').click()
    driver.find_element_by_id("file_upload").send_keys("E:\\Pictures\\lyp.jpg")
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="upload-pane"]/div[2]/button').click()
    time.sleep(3)
    driver.find_element_by_id('id_nick_name').clear()
    time.sleep(3)
    driver.find_element_by_id('id_nick_name').send_keys(u'漆来平猪')
    driver.find_element_by_id('id_position').clear()
    time.sleep(3)
    driver.find_element_by_id('id_position').send_keys(u'测试工程师猪')
    time.sleep(2)
    driver.find_element_by_id('id_description').clear()
    driver.find_element_by_id('id_description').send_keys(u'打酱油工程师')
    js="document.body.scrollTop=10000;"
    driver.execute_script(js)

    time.sleep(2)
    driver.find_element_by_id('id_qq').clear()
    driver.find_element_by_id('id_qq').send_keys('123456')
    time.sleep(2)

    driver.find_element_by_id('user_save').click()
    time.sleep(2)

    actual=select('select nickname from mz_forum_entity where user=2218 order BY date_publish  DESC limit 0,1 ;')
    print(actual)

    update_output('FPS_010','漆来平猪',actual)
setting(login.driver)