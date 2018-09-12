# _*_ coding:utf-8 _*_
__author__ = 'lilang'

from operator import add, sub
from random import randint, choice
from time import ctime, sleep
def test():
    # print 'hell,world'
    return 'test', 'hahaha', 'ssas'
    # return [1, 2, 3]


def cal():
    ops = {'+': add, '-': sub}
    MAXTRIES = 0
    op = choice('+-')  # 随机返回一个运算符
    nums = [randint(1, 100) for i in range(2)]
    nums = sorted(nums, reverse=True)
    ans = ops[op](*nums)
    while True:
        if int(input(str(nums[0])+str(op)+str(nums[1])+'=?')) == ans:
            print ('correct')
            return False

        else:
            print ('wrong')
            MAXTRIES += 1
            if MAXTRIES == 3:
                print ('The answer is '+str(ans))
                return False

    print (op, type(op), nums, ans)

def tsfunc(func):
    def wrappedFunc():
        print ('[%s] %s() called' % (ctime(), func.__name__))
        return func()
    return wrappedFunc 
@tsfunc
def foo():
    pass

def func():
    pass

if __name__ == '__main__':
    # s = test()
    # x, y, z = test()
    # (a, b, c) = test()
    # print x, y, z, a, b, c, s
    # print test()[0]
    cal()


