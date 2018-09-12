# _*_ coding:utf-8 _*_
__author__ = 'lilang'
import sys
import time
import random
def test():
    # my_dict = {}
    # new_dict = {1: 2, 3: 4}
    # print my_dict, new_dict, type(my_dict), type(new_dict)
    # fdict = dict((['x', 1], ['y', 2]))
    ddict = {}.fromkeys(('x', 'y'))
    # print fdict, ddict
    # for k in new_dict.keys():
    #     print k, new_dict[k]
    # if 'x' in ddict.keys():
    #     print ddict['x']
    # print cmp(ddict, ddict)
    # ddict_copy = ddict.copy()
    # ddict_copy['x'] = 'lilanglala'
    # print ddict, ddict_copy, len(ddict_copy)
    # print hash('li')
    dic_new = dict.fromkeys(('x', 'lang', 'hou'), ('test', 1, 2))
    print dic_new
    print dic_new.items(), dic_new.keys(), dic_new.values()
    print sorted(dic_new)
    dic_new.update(ddict)
    print dic_new, dic_new.get(1)

def test2():
    dict1 = {1: 789, 1.0: 'xyz'}
    print dict1
db = {}

def new_user():
    prompt = 'login desired: '
    while True:
        name = raw_input(prompt)
        if name in db.keys():
            print u'账号已存在，请重新输入'
            continue
        else:
            break
    pwd = raw_input('passwd: ')
    db[name] = pwd


def login():
    name = raw_input('login: ')
    pwd = raw_input('passwd: ')
    passwd = db.get(name)
    time_format = '%Y-%m-%d %X'
    now_time = time.strftime(time_format, time.localtime())
    if passwd == pwd:
        print 'welcome back', name
        db['login_time'] = now_time
    else:
        print u'用户名或密码不正确'
    print db
def show_menu():
    prompt = """
    (N)ew User Login
    (E)xisting User Login
    (Q)uit
    Enter choice:
    """
    methd = {'n': new_user, 'e': login}
    while True:
        while True:
            try:
                choice = raw_input(prompt).strip()[0].lower()
            except (EOFError, KeyboardInterrupt):
                choice = 'q'
            print '\nYou picked: [%s]' % choice

            if choice not in 'neq':
                print 'invalid option, try again'
            else:
                break
        if choice == 'q':
            break
        methd[choice]()



def test3():
    s = set('cheeseshop')
    # print s, type(s)
    t = frozenset('bookshop')
    h = set('bokshp')
    # print t, type(t), len(t),
    # for i in t:
    #     print i
    # s.add('gggg')
    # s.update('pypi')
    # s.remove('e')
    # print 'b' in s, s
    # s -= set('pypi')
    # s.clear()
    print s, '\n', t, '\n', h, '\n', s == t, t == h, s < t
    print s | t, type(t | s), s & t, s ^ t
    print set((1, 3, 4, 6, 7, 1))

def test71():
    a = {'a': 1, 'c': 2}
    b = {'d': 'lilang', 'b': 'test'}
    a.update(b)
    print a
    c = sorted(a)
    print c

def test74():
    a = [1, 3, 2]
    b = ['lilang', 'test', 'hou']
    s = dict(zip(a, b))
    print s
    time_format = '%Y-%m-%d %X'
    print time.strftime(time_format, time.localtime())


class Test78():
    def __init__(self):
        self.my_dic = {}
        self.new_dic = {}

    def update_list(self):
        staff_name = raw_input('enter staff name')
        staff_id = raw_input('enter staff id')
        self.my_dic[staff_id] = staff_name
        print self.my_dic

    def sort_id(self, sort_type):
        if sort_type == 'id':
            print sorted(self.my_dic.items(), key=lambda d: d[0])

        else:
            print sorted(self.my_dic.items(), key=lambda d: d[1])

    def chose(self):
        promt = u"""
        输入i,输入数据
        输入id,按id排序
        输入name,按name排序
        输入q,退出程序
        """
        while True:
            chosen = raw_input(promt)
            if chosen not in ['i', 'id', 'name','q']:
                print 'chose is error'
                continue
            elif chosen == 'i':
                self.update_list()
            elif chosen in ['id', 'name']:
                self.sort_id(chosen)
            else:
                break


def test79(a, b, c):
    b = b.lower()
    c = c.lower()
    r_list = []
    for i in c:
        if i.lower() not in a:
            r_list.append(i)
    for i in b:
        if i.lower() not in a:
            r_list.append(i)

    print ('').join(r_list)

def test713():
    s = set()
    x = set()
    for i in range(0, 10):
        s.add(random.randint(0, 9))
        x.add(random.randint(0, 9))
    print s, x, s | x, s & x

if __name__ == '__main__':
    test713()



