# _*_ coding:utf-8 _*_
__author__ = 'lilang'
import sys, os, errno, types, tempfile, math, cmath
def test_exp():
    try:
        f = open('122', 'r')
    except IOError as e:
        print (e)


def safe_float(a):
    # try:
    #     result = float(a)
    # # except (ValueError, TypeError):
    # except Exception, e:
    #     result = e
    # print result, type(e)

    try:
        result = float(a)
    except (ValueError, TabError) as e:
        # print e, type(e), e.__class__, e.__doc__, e.__class__.__name__
        result = str(e)
    return result
def card_dl():
    print ('test')
    log = open('card.log', 'w')
    try:
        f = open('llala2', 'r')
    except IOError as e:
        log.write('no data this month\n')
        sys.exit()
    else:
        print (u'ther is data this month\n')
    finally:
        print (u'整完了')
    lines = f.readlines()
    f.close()
    total = 0.00
    log.write('account log:\n')
    for i in lines:
        result = safe_float(i)
        if isinstance(result, float):
            total += result
            log.write('data... processed\n')
            print (u'余额', total)
        else:
            log.write('ignored: %s' % result)
            print ('$%.2f (new balance)') % total
    log.close()

def test_with():
    with open('lilan22g.txt', 'r') as f:
        for i in f:
            print (i.strip())

def test_assert():
    try:
        assert 1 == 2, 'One does not equal zero silly!'
    except AssertionError as e:
        print (e)

class NetworkError(IOError):
    pass

class FileError(IOError):
    pass

def upd_args(args, newarg=None):
    if isinstance(args, IOError):
        my_args = []
        my_args.extend([arg for arg in args])
    else:
        my_args = list(args)

    if newarg:
        my_args.append(newarg)
    return tuple(my_args)

def file_args(file, mode, args):
    if args[0] == errno.EACCES and 'access' in dir(os):
        perms = ''
        permd = {'r': os.R_OK, 'w': os.W_OK, 'x': os.X_OK}
        pkeys = permd.keys()
        pkeys.sort()
        pkeys.reverse()
        for eachPerm in 'rwx':
            if os.access(file, permd[eachPerm]):
                perms += eachPerm
            else:
                perms += '-'
        if isinstance(args, IOError):
            myargs = []
            myargs.extend([arg for arg in args])
        else:
            myargs = list(args)
            myargs[1] = "'%s' %s (perms: '%s')" % (mode, myargs[1], perms)
            myargs.append(args.filename)
    else:
        myargs = args
    return tuple(myargs)


def myopen(my_file, mode='r'):
    try:
        fo = open(my_file, mode)
    except IOError as args:
        raise (FileError, file_args(my_file, mode, args))
    return fo


def testfile():
    file_test = tempfile.mktemp()
    f = open(file_test, 'w')
    f.close()
    for eachTest in ((0, 'r'), (100, 'r'), (400, 'w'), (500, 'w')):
        try:
            os.chmod(file_test, eachTest[0])
            f = myopen(file_test, eachTest[1])
        except FileError as args:
            print (file_test, "%s: %s" % (args.__class__.__name__, args))
        else:
            print (file_test, "opened ok... perm ignored")
            f.close()
            os.chmod(file_test, 777)  # enable all perms
            # os.unlink(file_test)
def test_sys():
    try:
        float('as')
    except:
        out_put = sys.exc_info()
    print (out_put)
    for i in out_put:
        print (i)

def test105():
    # if 3 < 4 then: print '3 IS less than 4!' 语法错误
    # aList = ['Hello', 'World!', 'Anyone', 'Home?']
    # print 'the last string in aList is:', aList[len(aList)]  # 索引错误，超过最大边界
    # x = 4 % 0
    # print x   # 除0错误
    i = math.sqrt(0)  # 值错误，只能为正数或者0，求根方法
    print (i)


def test106(file_name, modle):
    try:
        f = open(file_name, modle)
    except IOError as e:
        f = None
    return f

def test107():
    try:
        f = open('lilang.txt', 'r')
        print (math.sqrt(-10))
    except IOError as e:
        print (e, 'pass')

    try:
        f = open('lilang.txt', 'r')
    except IOError as e:
        print (e, 'pass2')
    else:
        print (math.sqrt(-10))
def test109(a):
    try:
        r = math.sqrt(a)
    except ValueError as e:
        r = cmath.sqrt(a)
    print (r)
    return r


if __name__ == '__main__':
    test109(-1)
