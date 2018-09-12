# _*_ coding:utf-8 _*_
__author__ = 'lilang'
import sys
import math
import random



def test():
    i = 1
    j = 14214234L
    x = 1.33333333
    y = 1.23+4.56J
    print id(i), id(x)
    i += 1
    x = 2.444444
    print id(i), id(x)
    a = True
    print type(a)
    print sys.getwindowsversion()
    print 9999 ** 8
    print 2 >> 32
    print 4.3e25, 9.384e-23
    print y.real, y.imag, y.conjugate()
    s = x + j
    print s, type(s)
    print y + x
    print 1/2, 1.0/2.0, 1.0//2.0
    print 3**2, -3**2, 4**-1, 4**-2, 4**(-1), 4**-1
    print 30 & 45, 30 | 45
    a1 = ()
    a2 = []
    a3 = {}
    a4 = 0
    a5 = ''
    print bool(a1), bool(a2), bool(a3), bool(a4), bool(a5)
    print abs(-100.23), abs(int('1')),
    print coerce(1.11+1j, 11111111L), divmod(10, 2), divmod(11, 55), pow(10, 2, 33)
    print round(3, 5)
    for i in range(10):
        print round(math.pi, i)
    print oct(10), hex(10), chr(240), ord('p')

def test52(x, y):
    print int(x)*int(y)

def test53(grade):
    if 90 <= grade <=100:
        print 'A'
    elif 80 <= grade <90:
        print 'B'
    elif 70 <= grade < 80:
        print 'C'
    elif 60 <= grade < 70:
        print 'D'
    else:
        print 'F'

def test54(year):
    if int(year) % 4 == 0 and int(year) % 100 != 0 or int(year) % 400 == 0:
        print u'闰年'
    else:
        print u'不是闰年'


def test55(money):
    money = int(money)
    print money/25 + (money % 25)/10 + ((money % 25) % 10)/5 + ((money % 25) % 10) % 5


def test59():
    print 17+32, 017+032, 017+32, 56l+78l


def test510(a, b):
    for i in range(0, 21):
        if i % 2 == 0:
            print u'偶数', i
        elif i % 2 == 1:
            print u'奇数', i
    if int(a) % int(b) == 0:
        print str(a) + u'能被' + str(b) + u'整除'
    else:
        print str(a) + u'不能被' + str(b) + u'整除'

def test513():
    my_list = list()
    for i in range(100):
        my_list.append(random.randint(0, i))

    print len(my_list), my_list
    list_order = list()
    for j in range(len(my_list)-40):
        list_order.append(my_list[random.randint(0, j)])
    print list_order
    list_order.sort()
    print u'test', list_order

if __name__ == '__main__':
    test513()
