# -*- coding: utf-8 -*-
__author__ = 'admin'
from bid_by_pai_all import login
from pyquery import PyQuery as pq
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def chinese_math(content):
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

    match = zhPattern.search(content)
    if match:
        return content, 'True'
    else:
        return content, 'Fasle'

def get_newcookies():
    login_info = login('https://jc.yzw.cn', 'test5', '1111111q')
    Cookies = login_info[0]
    lan = Cookies._cookies['.yzw.cn']['/']['oc.web.auth.yzw'] # --prd
    # lan = Cookies._cookies['.yzw.cn.qa']['/']['web.auth.yzw']
    lan.name = 'LANGUAGE_CODE'
    lan.value = '6102BBC96AA9BFA058601B7E45F6A8E56D0D40C6E9F9B2E69466F8'
    # 546F9E8B927D7D8F932CE4A02BC4C267332F8BDEE9E6B4E6827BF8,6102BBC96AA9BFA058601B7E45F6A8E56D0D40C6E9F9B2E69466F8
    # qa 4D634E70B8689ECF2884348A3E992A62DE1B39202C5D11B48B44
    Cookies._cookies['.yzw.cn']['/']['LANGUAGE_CODE']=lan # --prd
    # Cookies._cookies['.yzw.cn.qa']['/']['LANGUAGE_CODE']=lan
    return Cookies


def get_list(url):
    Cookies = get_newcookies()
    contract = requests.post(url, cookies=Cookies)
    txt = pq(contract.text).text()
    txt = re.sub("(<!--.*?-->)", "", txt, flags=re.MULTILINE)
    txt = re.sub("^\s+\/\*.*", "", txt, flags=re.MULTILINE)
    txt = re.sub("^\s+\*.*", "", txt, flags=re.MULTILINE)
    txt = re.sub("\/\/.*", "", txt, flags=re.MULTILINE)
    txt = re.sub('[a-zA-Z0-9]', "", txt)
    txt = re.sub('[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]', "", txt).replace(' ', '').replace('\n', '').replace('\r', '')
    return txt

def all_list():
    f = open('lilang.txt', 'r')
    s = open('result.txt', 'w')
    my_list = f.readlines()
    for i in my_list:
        if len(i)>0:
            my_data = i.split(' ')
            url = 'https://jc.yzw.cn/'+my_data[0]
            result = get_list(url)
            s.write(my_data[1].replace('\n','')+' '+url+' '+result+'\n')
            print url, ' ', 'OK'
    f.close()
    s.close()





all_list()



