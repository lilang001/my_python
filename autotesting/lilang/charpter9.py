# _*_ coding:utf-8 _*_
__author__ = 'lilang'
import os
import sys

def file_test():
    filename = raw_input(u'随便输入点东西\n')
    fobj = open(filename, 'w')
    while True:
        aLine = raw_input("Enter a line ('.' to quit): ")
        if aLine != ".":
            fobj.write('%s%s' % (aLine, os.linesep))
        else:
            break
    fobj.close()

def test_move():
    f = open('llala', 'w+')
    print f.tell()
    f.write('line123456678901\n')
    print f.tell()
    f.write('test2123456678901\n')
    print f.tell()
    f.seek(-19, 1)
    print f.tell()
    print f.readline()
    f.seek(0)
    print f.tell(), f.readline()
    print f.tell(), f.readline()
    print f.fileno()
    f.close()


def sys_test():
    # f = open('lia', 'r')
    # print os.path('lia')
    # # print f.getctime()
    # raw_input('')
    print sys.argv, sys.stderr, sys.stdin, sys.stdout

    # 判断是否存在以下目录，一旦有就结束
    for tmpdir in (r'c:\temp', 'temp'):
        if os.path.isdir(tmpdir):
            print 'ok'
            break
        else:
            print 'no temp directory available'
    tmpdir = 'temp'
    os.chdir(tmpdir)  # 切换到该目录
    cwd = os.getcwd()  # 获取当前目录
    print u'当前目录是', cwd   # 打印当前目录
    os.mkdir('../example') # 在上级目录创建一个exmaple的目录
    os.chdir('../example')  # 切换到上级目录下的另一目录
    cwd = os.getcwd()  # 打印当前目录
    print u'最新的目录是', cwd
    print u'当前目录下有以下文件', os.listdir(cwd)  # 获取当前目录下的文件列表
    f = open('test', 'w')
    f.write('foo\n')
    f.write('bar\n')
    f.close()
    print u'当前目录有文件', os.listdir(cwd)
    os.rename('test', 'test_new56')  # 重命名文件问新的文件名
    print u'重命名后有文件', os.listdir(cwd)
    path = os.path.join(cwd, os.listdir(cwd)[0])
    print u'当前完整路径，包含第一个文件的名称', path
    print u'当前完整目录是', os.path.split(path)
    print u'当前目录是包含文件名', os.path.splitext(os.path.basename(path))

    # 按行打印当前目录第一个文件的内容
    s = open(path)
    for i in s:
        print i
    s.close()
    os.remove(path)  # 移除该文件
    print os.listdir(cwd), os.getcwd()  # 打印剩余的目录文件
    os.chdir('../')
    print os.getcwd()
    os.rmdir('example')  # 移除该目录

def test91():
    f = open('lilang.txt', 'r')
    for i in f:
        if i.strip()[0] != '#':
            print i.strip()
    f.close()

def test92(a, b):
    f = open(a)
    b = int(b)
    all_lin = f.readlines()
    # for i in f:
    #     if b > 0:
    #         print i
    #         b -= 1
    #     else:
    #         break
    for i in range(b):
        print all_lin[i]
    f.close()


def test93():
    f = open('lilang.txt', 'r')
    all_line = f.readlines()
    print len(all_line)
    f.close()

def test94():
    f = open('lilang.txt', 'r')
    n = 0
    for i in f:
        if n < 2:
            print i
            n += 1
            if n == 2:
                n = 0
                os.system('pause')   # 暂停程序功能
def test95():
    f = open('lilang.txt', 'r')
    s = open('llala', 'r')
    f_lines = f.readlines()
    s_lines = s.readlines()
    for i in range(len(f_lines) if len(f_lines) <= len(s_lines) else len(s_lines)):
        if f_lines[i] != s_lines[i]:
            print i, f_lines[i], s_lines[i]
            break
        else:
            continue

def test97():
    s = dir(sys)
    for i in s:
        print i, getattr(sys, i), type(getattr(sys, i))

def test98():
    path = 'D:\Python27\Lib'
    f = os.listdir(path)
    s = [x for x in f if x.endswith('py')]
    result = {}
    for i in s:
        f = open(path + os.sep + i, 'r')
        module = i[:-3]
        result.setdefault(module, '')
        doc = False
        for line in f:
            if line.strip().startswith('"""') and line.strip().endswith('"""'):
                result[module] += line
                f.close()
                break
            elif (line.strip().startswith('"""''"""') or line.strip().startswith('r"""')) and len(line) > 3:
                doc = True
                result[module] += line
                continue
            elif doc:
                if line == '"""':
                    result[module] += line
                    f.close()
                    doc = False
                    break
                else:
                    result[module] += line
            else:
                continue
    # print result
    # f = open(path + os.sep + 'ast.py', 'r')
    # print os.getcwd
    # for line in f:
    #     print line + 'end'
    #     # if line.strip().startswith('"""') and line.strip().endswith('"""'):
    #     #     result.append(('ast.py', line))
    #     #     break
    #     # else:
    #     #     continue
    print result

class money_manage():
    def __init__(self):
        # 初始化把文件现有的账户信息给读取出来
        self.f = open('count.txt', 'r+')
        self.count = {}
        for i in self.f:
            self.count = eval(i)
        print self.count
        self.f.close

    def save_money(self):
        count_type = raw_input(u'输入存款账户,cash,finance, regular')
        mount = raw_input(u'输入存款金额')
        if count_type not in ('cash', 'finance', 'regular'):
            print u'账户选择错误'
        elif int(mount) < 0:
            print u'金额不能小于0'
        else:
            config = raw_input(u'确认请按Y，取消请随意按')
            if config.upper() == 'Y':
                self.count[count_type] += int(mount)  # 存款减少
            print self.count
            f = open('count.txt', 'w')
            f.write(str(self.count))
            f.flush()
            f.close()

    def draw_money(self):
        count_type = raw_input(u'输入存款账户,cash,finance, regular')
        mount = raw_input(u'输入存款金额')
        if count_type not in ('cash', 'finance', 'regular'):
            print u'账户选择错误'
        elif int(mount) < 0:
            print u'金额不能小于0'
        elif int(mount) > self.count[count_type]:
            print u'麻痹余额不足也行取钱'
        else:
            config = raw_input(u'确认请按Y，取消请随意按')
            if config.upper() == 'Y':
                self.count[count_type] -= int(mount)  # 存款减少
            else:
                pass
            f = open('count.txt', 'w')
            f.write(str(self.count))
            f.flush()
            f.close()

    def chose_menu(self):
        choice = True
        while choice:
            chosen = raw_input(u'输入你的选择，S存钱，D取钱, Q退出')
            if chosen.upper() not in ('S', 'D', 'Q'):
                print u'your choice is incorrect'
            elif chosen.upper() == 'S':
                self.save_money()
            elif chosen.upper() == 'D':
                self.draw_money()
            elif chosen.upper() == 'Q':
                print u'you select quit, bye bye '
                choice = False
            else:
                continue

def test913():
    # print dir(os)
    # for i in dir(os):
    #     print i, getattr(os, i)
    print dir(sys.argv)


def test915():
    f = open('count.txt', 'r')
    f1 = open('lilang.txt', 'w')
    for i in f:
        f1.write(i)
    f.close()
    f1.close()

def test916():
    f = open('count.txt', 'r+')
    my_list = []
    for i in f:
        if len(i) > 80:
            my_list.append(i[0:79])
            my_list.append(i[80:-1])
        else:
            my_list.append(i)
    f.close()
    s = open('count.txt', 'w')
    for i in my_list:
        s.write(i.strip()+'\n')
    print my_list
    s.close()
if __name__ == '__main__':
    test916()
