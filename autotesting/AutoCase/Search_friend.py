# -*- coding: utf-8 -*-
__author__ = 'Maiziedu'

from selenium import webdriver
import time
import math
import datetime
import login
from selenium.webdriver.common.keys import Keys
from connectDB import update_output,select


def fans(driver):
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



def Add_friend(driver):
    username='qlp@qq.com'
    password='123123123'
    login.login_fps(username, password)
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[3]/div/ul/li[2]/a/span[1]').click()
    time.sleep(3)
    trupleFansCount0=select('select count(*) from fps_20151217.mz_common_usernetwork where userA in (select userB from fps_20151217.mz_common_usernetwork where userA=2218 ) AND userB=2218;')

    # 点击下拉按钮
    driver.find_element_by_xpath('//*[@id="jiaguanzhu"]').click()
    print( trupleFansCount0[0][0])

    time.sleep(3)
    trupleFansCount1=select('select count(*)from fps_20151217.mz_common_usernetwork where userA in (select userB from fps_20151217.mz_common_usernetwork where userA=2218 ) AND userB=2218')
    print(trupleFansCount1[0][0])
    intActual=trupleFansCount1[0][0]-1
    print(intActual)
    time.sleep(5)

    update_output('FPS_014',trupleFansCount0[0][0],intActual)





def Cancel_friend(driver):
    username='qlp@qq.com'
    password='123123123'
    login.login_fps(username, password)
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[3]/div/ul/li[1]/a/span[1]').click()
    time.sleep(3)
    trupleFansCount0=select('select count(*) from fps_20151217.mz_common_usernetwork where userA in (select userB from fps_20151217.mz_common_usernetwork where userA=2218 ) AND userB=2218;')
    print(trupleFansCount0[0][0])
    # 点击我的好友
    driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[1]/div/div/div/div[1]/ul/li[1]/a[2]').click()
    time.sleep(3)
    # 点击下拉按钮
    driver.find_element_by_xpath('//*[@id="MY_FRIEND"]/div/div[1]/div/div/div[2]/div[1]/div[2]/div/a/span').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="MY_FRIEND"]/div/div[1]/div/div/div[2]/div[1]/div[2]/div/ul/li/a').click()
    time.sleep(3)
    # 查询数据库
    trupleFansCount1=select('select count(*)from fps_20151217.mz_common_usernetwork where userA in (select userB from fps_20151217.mz_common_usernetwork where userA=2218 ) AND userB=2218')
    print(trupleFansCount1)
    intActual=trupleFansCount1[0][0]+1
    time.sleep(5)

    update_output('FPS_015',trupleFansCount0[0][0],intActual)
    print(intActual)

    # 搜索好友

Cancel_friend(login.driver)
# Add_friend(login.driver)