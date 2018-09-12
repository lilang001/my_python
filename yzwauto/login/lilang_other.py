# -*- coding: utf-8 -*-
__author__ = 'admin'
import math


# 求个中位数算法呵呵哒
def mid():
    a = (291.4000, 324.0000, 330.0000)
    a = sorted(a)
    print len(a)
    if len(a) % 2 == 0:
        md = a[len(a)/2-1]
    else:
        md = a[(len(a)+1)/2]
    print md
    my_list = list()
    for i in range(len(a)):
        if 0.3*md < a[i] < 1.7*md:
            my_list.append(a[i])
        else:
            pass
    print len(my_list)
    return my_list
# 计算分供商评分
def cal_supplier_score():
    summary = 100
    man_score = ()
    dy_score = ()
    print summary, man_score, dy_score,  ((50.5*0.31+0*0.69)*0.6+60*0.4)*752/9753 + (50.5*0.6+220/3*0.4)*9001/9753
    print ((82*1)*0.6+79*0.4)*800/(800+200) ,88.58*200/(800+200)

if __name__ == '__main__':
    cal_supplier_score()

