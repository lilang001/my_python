# _*_ coding:utf-8 _*_
__author__ = 'lilang'
import string
import copy
import keyword
import sys
from string import Template

def test():
    my_str = raw_input(u'输入一个至少两个长度变量名？')
    # # print my_str[0:10], my_str[::-1], my_str[::-2]
    # for i in [None] + range(-1, -len(my_str), -1):
    #     my_str[:i]
    # s = list(my_str)
    # a = ('a', '100', 'test', 'over')
    # a_str = str(a)
    # b_list = list(a)
    # print a_str, b_list, str(a)
    dg = string.digits
    alphas = string.letters + '_'
    # print dg, alphas
    if len(my_str) > 1:
        if my_str[0] not in alphas:
            print 'not OK'
        elif keyword.iskeyword(str(my_str)):
            print u'python 关键字'
        else:
            for i in my_str[1:]:
                if i not in dg + alphas:
                    print 'not ok'
                    break
                else:
                    print 'ok'

    else:
        print u'not OK'


def test2():
    my_str = '%s %s' % ('Spanish', 'Inquisition')
    print my_str
    s = '1'.join('lilang')
    print s
    new_s = '%s %s' % (s[:3], s[10])
    print new_s, type(new_s), string.upper(new_s)
    hl = 'Hello' 'world!'
    print hl
    u_str = 'Hello' + u'李朗 ' + 'World' + u'!'
    print u_str, u_str, u_str*3

def test3():
    s = '%f' % 1.555555555
    print s, type(s)
    m = 'There are %(lang)s %(howmany)d Quotation Symbols' % {'lang': 'Python', 'howmany': 3}
    print m
    s2 = Template('There are ${howmany} ${lang} Quotation Symbols')
    print s2.substitute(lang='Python', howmany=3)
    print s2.safe_substitute(lang='Python')

def test4():
    print r'/n', u'abc', ur'Hello\nWorld!'
    s, t, g = 'fofff1', 'obr2', 'lilang'
    nex = zip(s, t, g)
    print nex
    print string.capitalize(s)
    print string.center(s, 10), string.count(s, 'f'), s.find('f', 5, 5), s.isalnum()


def test_list():
    s = list('foo')
    print s, s[0:1], s[1:3]
    s[2] = 'test'
    print s
    s.append(('lilang', 'jiangyou'))
    print s
    del s[0]
    print s
    s.remove('test')
    print s
    h = [i * 2 for i in s]
    print h
    test_li = [1]
    test_li.insert(0, 154)
    test_li.append('lilanglalal')
    # print test_li
    # print 0 in test_li, '1' in test_li, test_li.index(1),
    # print test_li.index('lilangl1alal')
    for i in test_li:
        print test_li.index(i),
    test_li.sort()
    print test_li
    test_li.reverse()
    print test_li
    test_lanmg = ['as ', 'noye', 14]
    test_li.extend(test_lanmg)
    print test_li



stack = []

def pushit():
    stack.append(raw_input('Enter new string: ').strip())

def popit():
    if len(stack) == 0:
        print 'Cannot pop from an empty stack!'
    else:
        print 'Removed [', stack.pop(0), ']'

def viewstack():
    print stack  # calls str() internally

CMDs = {'u': pushit, 'o': popit, 'v': viewstack}

def showmenu():
    pr = """
    p(U)sh
    p(O)p
    (V)iew
    (Q)uit
    Enter choice: """
    while True:
        while True:
            try:
                choice = raw_input(pr).strip()[0].lower()
            except (EOFError, KeyboardInterrupt, IndexError):
                choice = 'q'
                print '\nYou picked: [%s]' % choice
            if choice not in 'uovq':
                print 'Invalid option, try again'
            else:
                break
        if choice == 'q':
            break

        CMDs[choice]()

def test_tuple():
    t = ('li', 'lang', 'hou', 'xin')
    print t[0], t[1], t[2], t[3], t[0:3]
    t1 = t[0:1] + t[0:3]
    print t1
    print t*2, 'li' in t1, (t*100).count('li')
    st1 = str(t*100)
    print type(st1), max(st1), t1 < t, t < t1
    x, y = 1, 2
    print type((x, y))

def test_change():
    person = ['name', ['saving', 100.00]]
    husb = person[:]
    wife = copy.deepcopy(person)
    s = [type(i) for i in person, husb, wife]
    husb[0] = 'li'
    wife[0] = 'hou'
    husb[1][1] = 30.00
    print husb, wife

def test61():
    s = 'lilang'
    b = 'xxx'
    print b in s, 'lil' in s

def test63():
    s = raw_input(u'请输入一串数字,多个以逗号隔开')
    s = s.split(',')
    s_new = []
    for i in s:
        s_new.append(float(i))
    print s, type(s), s_new
    s_new.sort(reverse=True)
    s_new.sort()
    print s_new
    sorted(s_new, reverse=True)
    print s_new

def test64(my_str):
    r = len(my_str) - 1
    l = 0
    while my_str[l] == ' ':
        l = l + 1
    while my_str[r] == ' ':
        r = r - 1
    result = my_str[l:r+1]
    print result

def test67():
    # 要求用户输入一个整数
    num = raw_input(u'请输入一个整数')
    # 将str类型的num转换为int型
    num = int(num)
    # 从1到num+1，生成一个list
    fac_list = range(1, num+1)
    print type(fac_list), fac_list
    print "BEFORE:", fac_list
    i = 0
    while i < len(fac_list):
        del fac_list[i]
        i += 1
    print "AFTER:", fac_list

def test610(my_str):
    my_str = str(my_str)
    new = []
    for i in my_str:
        if i.isupper():
            new.append(string.lower(i))
        elif i.islower():
            new.append(string.upper(i))
        else:
            new.append(i)

    new = ('').join(new)
    print new

def test610(my_str):
    my_str = str(my_str)
    new = []
    for i in my_str:
        if i.isupper():
            new.append(string.lower(i))
        elif i.islower():
            new.append(string.upper(i))
        else:
            new.append(i)

    new = ('').join(new)
    print new

def test6120(my_str, key_word):
    my_str = list(my_str)
    if key_word in my_str:
        return my_str.index(key_word)
    else:
        return -1


if __name__ == '__main__':
    print test6120(('1', 'lilangss.sdds', '2', 'li'), 'li')
