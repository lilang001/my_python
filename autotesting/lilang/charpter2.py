# _*_ coding:utf-8 _*_
__author__ = 'Administrator'
import sys

def test_if():
    x = 100
    if x >= 100:
        print (x)
    elif x < 100:
        print (100-x)
    else:
        print (u'我也不知道了')

def test_while():
    x = 1
    while x < 100:
        print (x)
        x += 1

def test_for():
    test_str = 'lilangblabal'
    for i in test_str:
        print (i),

def test_enumate():
    my_str = 'lilang is lilang'
    for i, j in enumerate(my_str):
        print (i, j)
def test27():
    my_str = input('请输入一个字符串，我会打印出来\n')
    for i in my_str:
        print (i),
    x = 0
    while x < len(my_str):
        print my_str[x]
        x += 1
def test289():
    a = (1, 2, 3, 4, 5)
    b = [1, 2, 3, 4, 6]
    print type(a), type(b)
    sum_i = 0
    for i in a:
        sum_i += i
    print sum_i/len(a)
    sum_j = 0
    for i in b:
        sum_j += i
    print float(sum_j)/len(b)

def test210():
    n = int(raw_input('Please input a number:'))
    while n <= 0 or n > 100:
        n = int(raw_input('Wrong number,Please input a number:'))
    print n

def test211():
    print u"选择1，输入5个数求和\n选择2，输入5个数求平均值\n输入0，退出\n输入其他数，无效\n"
    while True:
        select = int(raw_input(u'请选择\n'))
        if select == 1:
            a = int(raw_input(u'请输入第一个\n'))
            b = int(raw_input(u'请输入第二个\n'))
            c = int(raw_input(u'请输入第三个\n'))
            d = int(raw_input(u'请输入第四个\n'))
            e = int(raw_input(u'请输入第五个\n'))
            print a+b+c+d+e
        elif select == 2:
            a = int(raw_input(u'请输入第一个\n'))
            b = int(raw_input(u'请输入第二个\n'))
            c = int(raw_input(u'请输入第三个\n'))
            d = int(raw_input(u'请输入第四个\n'))
            e = int(raw_input(u'请输入第五个\n'))
            print float(a+b+c+d+e)/5
        elif select == 0:
            print u'程序退出了'
            break
        else:
            print u'输入错误，请重新输入'


def test212():
    print dir(), dir, type, type(dir), type(dir()), dir.__doc__, 'end'
    print dir(__doc__)

def test213():
    print dir(sys)
    print sys.version_info
    sys.exit()
    print sys.platform

if __name__ == "__main__":
    test213()
