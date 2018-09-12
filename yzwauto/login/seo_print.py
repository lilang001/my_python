# coding=utf-8
# @Author: Bing.B.Yan <yanbin>
# @Date:   2016-10-20T20:45:44+08:00
# @Email:  Bing.B.Yan@yzw.cn
# @Last modified by:   yanbin
# @Last modified time: 2016-11-02T12:47:40+08:00

from selenium import webdriver
import time
from login import login

def SeoList(file, user, pwd):
    f = open(file, 'r')
    url_list = f.readlines()
    result_list = list()
    if user == '':
        driver = webdriver.Chrome()
    else:
        driver = login(user, pwd)
        time.sleep(2)
    f.close()
    for i in url_list:
        try:
            print i
            driver.get(i)
            # Check Meta data
            meta_list = driver.find_elements_by_xpath("//meta")
            title = driver.title.encode("utf-8")
            if len(meta_list) > 1:
                for item in meta_list:
                    if item.get_attribute("name") == "keywords" or item.get_attribute("name") == "description":
                        if item.get_attribute("content").encode("utf-8") and item.get_attribute("name") == "keywords":
                            key_content = item.get_attribute("content").encode('utf-8')
                        elif item.get_attribute("content").encode("utf-8") and item.get_attribute("name") == "description":
                            desc_content = item.get_attribute("content").encode('utf-8')
                            print 'OK'

                        else:
                            key_content = 'no key error'
                            desc_content = 'no desc error'
                            print 'no data error'
            else:
                key_content = 'no meta error'
                desc_content = 'no meta error'
                print 'no bb error'
            result_list.append((i, title, 'key', key_content, 'desc', desc_content))
            time.sleep(2)

        except Exception as e:
            print e
    print result_list
    driver.close()
    return result_list

if __name__ == '__main__':
    SeoList('jc_login_url.txt', 'jcadmin', '111111')