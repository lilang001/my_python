# _*_ coding:utf-8 _*_
__author__ = 'lilang'

import os

def test():
    x, y = 3, 4
    s = x**2 if x < y else y
    print s
    count = 0
    while count < 9:
        print 'the index is:', count
        count += 1


def pwd_check():
    pwd_list = ['lilang', 'niuje', 'zhouyou']
    count = 3
    while count > 0:
        pwd = raw_input(u'Enter your password')
        if pwd in pwd_list:
            print 'Your pass word is right'
            continue
        else:
            print 'Your pass word is wrong, you can try'+str(count-1)+'time'
            count -= 1
def test_iter():
    s = ('a', 'b', 'c')
    s = iter(s)
    my_dic = {'1': 'lilang', '2': 'niuie', '3': 'zhouiy'}
    for i in my_dic.iteritems():
        print i
    d = [x for x in my_dic if x == '1']
    g = [x ** 2 for x in range(6)]
    g2 = filter(lambda x: x**2, range(6))
    x = [(x**2, y**2, z*2) for x in range(3) for y in range(5)  for z in range(10)]
    print x

def test_file():
    f = open('lilang.txt', 'r')
    # for i in f:
    #     print i
    print len([word for line in f for word in line.split()])
    print os.stat('lilang.txt').st_size
    f.seek(0)
    print sum(len(word) for line in f for word in line.split())
    f.close()

def cols(): # example of simple generator
    yield 56
    yield 2
    yield 1

def born():
    print [x**2 for x in range(10) if x % 2]
    print (x**2 for x in range(10) if x % 2)
    rows = [1, 2, 3, 17]
    s = ((i, j) for i in rows for j in cols())
    print s
    for x in s:
        print x

def max_file_len():
    f = open('lilang.txt', 'r')
    my = []
    for i in f:
        my.append(len(i))
    print max(my)
    f.seek(0)
    all_line = max(len(x.strip()) for x in f)
    print all_line
    f.close()

def test82(a, b, c):
    print range(a, b, c)

def test84(a):
    a = int(a)
    result = []
    for i in range(1, a+1):
        if a % i == 0:
            result.append(i)
    print result
    if len(result) == 2:
        print True
    else:
        print False

def test86(a):
    a = int(a)
    result = []
    test = True
    while test:
        for i in range(2, a+1):
            if a % i == 0:
                result.append((i))
                if a == i:
                    test = False
                a /= i
                break
            else:
                pass
    print sorted(result)

def test87(a):
    a = int(a)
    result = []
    for i in range(1, a):
        if a % i == 0:
            result.append(i)
    print result, sum(result)
    if sum(result) == a:
        print True
    else:
        print False

def test88(a):
    x = 1
    for i in range(1, a+1):
        x *= i
    print x

def test89(a):
    x = [0, 1]
    if a > 2:
        for i in range(2, a+1):
            x.append(x[i-1] + x[i-2])
        print x[-1], x
    else:
        print 1

def test811():
    choice = True
    f = open('811.txt', 'w+')
    while choice:
        chosen = raw_input(u'给出你的选择，I为出入一行数据,Q为退出')
        if chosen.upper() == 'I':
            content = raw_input(u'按姓,名的标准格式输出')
            x = [i for i in content.split(',')]
            if len(x) == 2:
                f.writelines(str(x) + '\n')
            else:
                print u'麻痹，格式不对'
                continue
        elif chosen.upper() == 'Q':
            choice = False
            print u'你选择了退出，拜拜'
        elif chosen.upper() == 'P':
            f.flush()
            f.seek(0)
            for x in f:
                print x
        else:
            print u'选择错误'
            pass

    f.close()

def test812():
    for i in range(2, 100):
        print i, bin(i), chr(i), oct(i)


if __name__ == '__main__':
    test812()
