# -*- coding: utf-8 -*-
__author__ = 'admin'
from random import randint,choice
from string import ascii_lowercase
from sys import maxsize
from time import ctime
import re

def gendata():
    doms = ('com','edu','net','org','gov')
    for i in range(randint(5,10)):
        dint = randint(0,maxsize)
        d_date= ctime(dint)
    shorter = randint(4,7)
    em = ''
    for j in range(shorter):
        em += choice(ascii_lowercase)
    longer = randint(shorter,12)
    dn =''
    for k in range(longer):
        dn+= choice(ascii_lowercase)
    print ('%s::%s@%s.%s::%d-%d-%d'%(d_date,em,dn,choice(doms),dint,shorter,longer))
    return '%s::%s@%s.%s::%d-%d-%d'%(d_date,em,dn,choice(doms),dint,shorter,longer)



def re_deal(rule):
    s = gendata()
    re_result = re.match(rule,s)
    if hasattr(re_result,'group')==True:
        result =re_result.group()
        print (result)
        return result
    else:
        print ('no macth！')



if __name__ == '__main__':
    rule_week = "^Mon|^Tue|^Wed|^Tur|^Fri|^Sta|^Sun"
    new_rule_week = "(Mon|Tue|Wed|Tur|Fri|Sta|Sun)"
    s = re_deal(new_rule_week)
    re.match('.+\d+-\d+-\d+',gendata())
    re.search('\d+-\d+-\d+',gendata())
    re.match('.+::(\d+-\d+-\d+)',gendata()).group(1)
    re.match('.+?(\d+-\d+-\d+)',gendata()).group(1)
    re.match('.+-(\d+)-',gendata()).group(1)
