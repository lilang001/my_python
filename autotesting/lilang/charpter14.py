# -*- coding: utf-8 -*-
__author__ = 'admin'
import sys
import os

def foo():
    pass

def test_bifs():
    print (type.__doc__,type.__name__,type.__module__)
    print (dir(type))


def lambdaFunc(x):
    if type(x)==int:
        return lambda x:x*2
    else:
        return "please give a int "


class C(object):
    def foo(self):
        pass

# 调用类的实例

class D(object):
    def __call__(self, *args):
        print ("im callable")

# 进程
def os_test():
    ret = os.fork()
    return os.system('dir')




if __name__ == '__main__':
    # test= test_bifs()
    # print (type(foo))
    # x= lambdaFunc(23.1)
    # print (x)
    # print (dir([].append))
    # c =C()
    # print (type(C), type(c), type(C.foo), type(c.foo))
    d =D()
    print ((d,),d(),d(3),d(3,'testli'))
    print (callable(D))
    # eval_code
    eval_code = compile('100+200','','eval')
    print ('eval_code:',eval (eval_code))
    single_code = compile('print ("hello, boy ")','','single')
    exec (single_code)
    exec_code  =compile("""
result= True
while result==True:
    req = input("count how many numbers?")
    try:
        for i in range(int(req)):
            print (i)
        result =False
    except:
        print ("please input an interger")
    """,'','exec'
    )
    exec (exec_code)
    # print (eval('"a"+"b"' ))
#     exec( """
# print ("lilangtest")
#     """)


# page601




