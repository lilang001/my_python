# coding = utf8
__author__ = 'Administrator'
# from selenium import webdriver
# import time
# web = webdriver.Firefox()
# base_url = 'http://192.168.1.142/group/ask'
# web.get(base_url)
# web.find_element_by_xpath('//*[@id="microoh-navbar-collapse"]/div[1]/div/a[1]').click()
# time.sleep(3)
# web.find_element_by_id("id_account_l").send_keys('username')
# web.find_element_by_id("id_password_l").send_keys('password')
from selenium import webdriver
import time
web = webdriver.Firefox()
web.maximize_window()
base_url = 'http://192.168.1.142/group/ask'
web.get(base_url)
web.find_element_by_xpath('//*[@id="microoh-navbar-collapse"]/div[1]/div/a[1]').click()
web.find_element_by_id("id_account_l").send_keys('qlp@qq.com')
web.find_element_by_id("id_password_l").send_keys('123123123')
time.sleep(3)
web.find_element_by_id("login_btn").click()
time.sleep(3)
nickname = web.find_element_by_xpath('/html/body/div[3]/header/div/div[2]/div[1]/div[1]/dl/dt/a[2]/span').text
print(nickname)