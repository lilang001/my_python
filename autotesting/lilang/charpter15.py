# -*- coding: utf-8 -*-
__author__ = 'admin'
#page637
import requests
from pyquery import PyQuery as pq
import re

def re_test(match_str,str, model):
    #r= requests.get('https://www.163.com/').text
    #a = pq(r)('body')('.index2017_wrap')('.ne_area')('.cm_area ')('.col_c ')('.mod_news_tab')('.tab_main ')('.cm_ul_round')('li')
    # re.match('foo','fooafooafoof')  # 匹配某个字符串
    # re.match('foo|fooa','fooafooafoof')  # 匹配某个两个正则表达式之一
    # re.match('.','fooafooafoof')  # 匹配任何字符（换行符除外）
    # re.match('^fooa','fooafooafoof') # 匹配开始
    # re.match('foof$','fooafooafoof') # 匹配结尾
    # re.match('fooa*','fooafooafoof') # 匹配出现0次或者N次
    # re.match('fooa+','fooafooafoof') # 匹配出现0次或者N次
    # re.match('foo?a','fooafooafoof') #
    # re.match('f{1}','fooafooafoof') # 匹配
    # re.match('[0-9]{5,9}','11233') # 匹配出现0次或者N次
    # re.match('[A-Za-z]{5,9}','fooafooafoof') # 匹配出现0次或者N次
    # re.match('[abc]','cooafooafoof')
    if model =='match':
        s = re.match(match_str,str)
        if s!=None:
            print (s.group())
            return s.group()
        else:
            print ('no ,match')
    elif model == 'search':
        s = re.search(match_str,str)
        if s!=None:
            print (s.group())
            return s.group()
        else:
            print ('no ,match')
    else:
        print ('model error')



if __name__ == '__main__':
    s = '[cr][23][dp][o2]'
    b = 'r2d2|c3po'
    patt = '\w+@(\w+\.)?\w+\.com'
    patt2 ='\w'
    patt3 = '(\w\w\w)-(\d\d\d)'
    # re_test('\w+@(\w+\.)?\w+\.com','nobo@xxx.com','match')
    # re_test('\w','1','match')
    # re.search(patt3,'111-222').group(2)
    # re.match('111','111-222').groups()
    re.findall('(c)(a)','scarycarcar')
    re.sub('x','mr.lilang','abvxaa')
    re.subn('x','mr.lilang','abvxaxa')
    re.split('a','bc,abd,aaa')
