# -*- coding: utf-8 -*-
__author__ = 'admin'


import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# 登录脚本
url = 'http://portal.jc.yzw.cn.qa:8000/'
# url = 'http://jctest.yzw.cn:16000/'
def login(user, pwd):

    driver = webdriver.Chrome()
    driver.get(url)
    # driver.maximize_window()
    driver.find_element_by_xpath('/html/body/div/div[3]/div/div/form/div[2]/input').send_keys(user)
    driver.find_element_by_xpath('/html/body/div/div[3]/div/div/form/div[3]/input').send_keys(pwd)
    driver.find_element_by_xpath('//*[@id="btnsubmit"]').click()
    return driver

# 报名
def sign_up(user, pwd, pid, sid):
    driver = login(user, pwd)
    time.sleep(1)
    url = 'http://vendor.yzw.cn.qa:8000/VendorPortal/Bidding/Detail?tenderSysNo='+pid+'&supplierSysNo='+sid
    # url = 'http://vendortest.yzw.cn:16000/VendorPortal/Bidding/Detail?tenderSysNo='+pid+'&supplierSysNo='+sid
    time.sleep(3)
    driver.get(url)
    time.sleep(2)
    try:
        driver.find_element_by_link_text('签收公告').click()
        time.sleep(2)
    except:
        pass
    try:
        driver.find_element_by_link_text('我要报名').click()
    except:
        driver.find_element_by_link_text('签收公告').click()
        time.sleep(4)
        driver.find_element_by_link_text('我要报名').click()
    time.sleep(1)
    driver.close()

# 投标
def tender(user, pwd, pid, sid):
    driver = login(user, pwd)
    time.sleep(3)
    tender_url = 'http://vendor.yzw.cn.qa:8000/VendorPortal/Bidding/Detail?tenderSysNo='+pid+'&supplierSysNo='+sid
    # tender_url = 'http://vendortest.yzw.cn:16000/VendorPortal/Bidding/Detail?tenderSysNo='+pid+'&supplierSysNo='+sid
    time.sleep(2)
    driver.get(tender_url)
    time.sleep(2)
    try:
        driver.find_element_by_link_text('签收招标文件').click()
        time.sleep(2)
        driver.find_element_by_link_text('签收招标文件').click()
        time.sleep(2)
    except :
        pass
    time.sleep(3)
    driver.find_element_by_link_text('我的投标文件').click()
    time.sleep(2)
    driver.find_element_by_link_text('我的投标文件').click()
    time.sleep(2)
    el = driver.find_elements_by_class_name('input-sm')
    try:
        for i in range(len(el)):
            el[i].clear()
            el[i].send_keys(random.randint(-100, 200))
        time.sleep(1)
    except:
        for i in range(len(el)):
            el[i].clear()
            el[i].send_keys(random.randint(-100, 200))
        time.sleep(1)
    driver.find_element_by_xpath('//div/a/span[text()="投标"]').click()
    time.sleep(1)
    #driver.close()


if __name__ == '__main__':
    tender('sup100', '111111', '539202', '1004120')
    # login('1', '2')
