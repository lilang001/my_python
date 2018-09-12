# coding utf-8
from selenium import webdriver
import time
import unittest
class test_yzw_login(unittest.TestCase):

    def getLogininfo(self):
        f = open("user.txt", 'r')
        Logininfo = f.readlines()

        for i in Logininfo:
            Logininfo_detail = i.split(' ')
            try:
                self.Login(Logininfo_detail[0], Logininfo_detail[1])
                print Logininfo_detail[0], 'pass'
                time.sleep(5)
            except:
                print Logininfo_detail[0], 'error'

    def Login(self, username,pwd):
        url = 'http://auth.yzw.cn.qa:8000/'
        driver = webdriver.Chrome()
        driver.get(url)
        driver.find_element_by_id('tbaccount').send_keys(username)
        driver.find_element_by_id('tbpassword').send_keys(pwd)
        driver.find_element_by_id('btnsubmit').click()
        driver.quit()

if __name__ == '__main__':
    test_yzw_login.getLogininfo()
