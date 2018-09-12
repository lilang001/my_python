# coding=utf-8
from pyse import Pyse, TestRunner
from time import sleep
import unittest
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

class BaiduTest(unittest.TestCase):

    def test_baidu(self):
        ''' baidu search key : pyse '''
        driver = Pyse("chrome")
        driver.open("https://www.baidu.com/")
        driver.clear("id=>kw")
        driver.type("id=>kw", "pyse")
        driver.click("css=>#su")
        sleep(1)
        assert("sssss")
        self.assertTrue("pyse",driver.get_title())
        driver.quit()


if __name__ == '__main__':
    print(dir_path)
    runner = TestRunner()
    runner.run()


