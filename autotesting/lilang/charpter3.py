# _*_ coding:utf-8 _*_
__author__ = 'Administrator'

import os
import keyword
def test1():
    print 'lillang',\
    'test'
    print keyword.iskeyword('print')
    print dir(keyword)
    print keyword.kwlist
    print keyword.__doc__

class FileTest():
    def __init__(self):
        self.name = ''
        self.content = ''

    def file_input(self):
        f_name = raw_input(u'请输入一个文件名')
        content = list()
        i = 1
        while True:
            if os.path.exists(f_name) and i < 2:
                print "ERROR: '%s' already exists" % f_name
                i -= 1
            else:
                break

        while True:
            entry = raw_input(u'请输入 ')
            if entry == '.':
                break
            else:
                content.append(entry)
        fobj = open(f_name, 'w')
        fobj.writelines(['%s%s' % (x, f_name) for x in content])
        fobj.close()
        print 'DONE!'

    def file_open(self):
        file_name = raw_input(u'请重新输入你要打开的文件名\n')
        try:
            f_open = open(file_name, 'r')
        except IOError, e:
            print e
        else:
            for i in f_open:
                print i
            f_open.close()



if __name__ == '__main__':
    FileTest().file_open()