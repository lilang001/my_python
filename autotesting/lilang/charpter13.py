# -*- coding: utf-8 -*-
__author__ = 'admin'
# from unitest import *
from time import time, ctime
class MyDataWithMethod(object):  # 定义类
    'address book entryy class'
    def __init__(self, nm, ph):  # 定义构造器
        self.name = nm
        self .phone = ph
        print ('Create instance for :', self.name)

    def updatePhone(self, newph):  # 定义方法
        self.phone = newph
        print ('Updated phone# for:', self.name)

    # def printFoo(self):  # 定义方法
    #     print 'You invoked printFoo()!'

# myObj = MyDataWithMethod()
# myObj.printFoo()

# john = MyDataWithMethod('llang', '6888')
# print john.name, john.phone
# john.updatePhone('132412421')
# print john.phone
# jane = MyDataWithMethod('Jane Doe', '650-555-1212')
class EmpMydata(MyDataWithMethod):
    def __init__(self, nm, ph, id, em):
        MyDataWithMethod.__init__(self, nm, ph)
        self.emid = id
        self.email = em
    def updateEmail(self,newem):
        self.email = newem
        print ('Upadatd  e-mail  address for:', self.name)
#
# john = EmpMydata('John Doe', '408-555-1212',42, 'john@spam.doe')
# print john.name, john.phone
# john.updatePhone('777')
# print john.phone
# john.updateEmail('8782')
# print john.email

# print EmpMydata.__class__, MyDataWithMethod.__doc__
# emmydate = MyDataWithMethod('1','2')
# print type(emmydate), type(0),type(MyDataWithMethod)
class P(object):
    def __del__(self):
        print ('deleted')

class C(object):  # 类申明
    def __init__(self):  # 构造器
        print ('begin')

# c1 = C()
# c2 = c1
# c3 = c1
# print id(c1), id(c2), id(c3)
# del c1
# del c2
# del c3

class InstCt(object):
    count = 0

    def __init__(self):
        InstCt.count+=1

    def __del__(self):
        InstCt.count-=1

    def howMany(self):
        print (InstCt.count)

# a = InstCt()
# b = InstCt()
# a.howMany()
# b.howMany()
# a.howMany()
# del a
# b.howMany()


class HotelRoomCalc(object):
    'Hotel room rate calculator'
    def __init__(self, rt, sales=0.085, rm=0.1):
        self.salesTax = sales
        self.romTax = rm
        self.roomRate = rt

    def calToal(self, days=1):
        daily = round(self.roomRate*(1+self.romTax+self.salesTax), 2)
        return float(days)*daily
#
# x = 3+0.14j
# print dir(x), x.__abs__(), x.imag, x.real, x.conjugate()

class Foo(object):
    x = 1.5
    y = {2003: 'poe2'}

# foo = Foo()
# print foo.x, foo.y
# foo.x = 1.7
# foo.y[2005] = 'valid path'
# print foo.x, Foo.x, foo.y, Foo.y




class P(object):
    def foo(self):
        print ('P print OK')

class C(P):
    def foo(self):
        print ('C print ok')

class AddrBookEntry(object):
    'address book entry class'
    def __init__(self, nm, ph):
        self.name = nm
        self.phone = ph
        print ('create instance for:', self.name)

    def updatePhone(self, newph):   # 定义更新号码方法
        self.phone = newph
        print ('Updated phone# for:', self.name, self.phone)


class EmpAddrBookEntry(AddrBookEntry):
    def __init__(self, nm, ph, id, em):
        AddrBookEntry.__init__(self, nm, ph)
        self.empid = id
        self.email = em

    def updateEmail(self, newem):
        self.email = newem
        print ('Updated email# for:', self.name, self.email)

# c = C()
# c.foo()
# P.foo(c)
#john = AddrBookEntry('li lang', '028-232333')
# jane = EmpAddrBookEntry('james bone', '028-666666', '12', 'lilang@qq.com')
# print dir(jane)

# 类属性测试,存在遮挡的效果，更新类实例不会影响类本身属性
class Foo(object):
    x =1.5

foo =Foo()

# print foo.x, Foo.x
# Foo.x = 1.7
# print foo.x, Foo.x
foo.x = 1.6
# print foo.x
# del foo.x
# print foo.x

# 类属性可变的测试,不存在遮挡的效果，更新类实例会影响类本身属性，无法del

# class TestFoo(object):
#     x = {2003: 'lilang'}
#
# test_foo = TestFoo()
# print test_foo.x
# test_foo.x[2004] = 'houhou'
# print test_foo.x, TestFoo.x
# del test_foo.x

# 静态方法测试

# class TestStaicMethod:
#     # @staticmethod  #函数修饰符正确方法
#     def foo():
#         print 'calling static method foo'
#     foo = staticmethod(foo)
#
# class TestClassMethod:
#     # @staticmethod  #函数修饰符正确方法
#     def foo():
#         pass
#         # print 'call class method foo() by tcm'
#     print 'foo() is part of class:', foo.__class__
#     foo = staticmethod(foo)

# tsm = TestStaicMethod()
# tsm.foo()
# TestStaicMethod().foo()
#
# tcm = TestClassMethod()
# tcm.foo()
#

# 通过继承覆盖父类方法 ,supper的用法，不需要父类的任何名称，直接调用自身即可，注意__init__方法也适用

class Parent(object):
    def foo(self):
        print ('hi, i am  P-foo()')

class Child(Parent):
    def foo(self):
        super(Child, self).foo()
        print ('hi, i am  C-foo()')

# P = Parent()
# P.foo()
# C = Child()
# C.foo()
# Parent.foo(C)

# 13.11.3 标准类派生和继承

class RoundFloat(float):
    def __new__(cls, val):
        return float.__new__(cls, round(val, 2))

# print RoundFloat(1.44444)

# 13.11.4 --参考page 517 多重继承,旧的先找直接上级--上上级--上上级的兄弟 ; 新式 找上级--上级兄弟--再上上级--再上上级兄弟，广式搜索法

# 13.12
# print issubclass(RoundFloat, float)  # A是否是B的子类或者子孙类
# print isinstance(Parent, object)   # A是否是B的实例

# 其他更多內建函数page 524

# 13.13 用特殊方法定制类 截止531

class RoundFloatManual(object):
    def __init__(self, value):
        assert isinstance(value, float) ,'Value must be a folat~'
        self.value = round(value, 2)

    def __str__(self):
        return '%.2f' % self.value
    __repr__ = __str__

# print RoundFloatManual(5.5999)
# print RoundFloatManual(5.1265)
# print RoundFloatManual('abcd')

# 13.13.2 数值定制
class Time60(object):
    def __init__(self, hr, min):
        self.hr = hr
        self.min = min

    def __add__(self, other):
        return self.__class__(self.hr+other.hr, self.min+other.min)

    def __iadd__(self, other):
        self.hr += other.hr
        self.min += other.min
        return self

    def __str__(self):
        return '%d:%d' %(self.hr, self.min)
    __repr__ = __str__
#
# print Time60(10, 23)
# print Time60(1110, 23)
# print Time60(10, 23)+Time60(110, 23)

# mon = Time60(10, 30)
# tue = Time60(11, 14)
# print mon, id(mon)
# mon += tue
# print mon , id(mon)

# 13.13.3 迭代器

class AnyIter(object):
    def __init__(self, data, safe=False):
        self.safe = safe
        self.iter = iter(data)

    def __iter__(self):
        return self

    def next(self, howmany=1):
        retval = []
        for eachItem in  range(howmany):
            try:
                retval.append(self.iter.next())
            except StopIteration:
                if self.safe:
                    break
                else:
                    raise

        return retval

# a = AnyIter(range(10))
# i = iter(a)
# for j in range(1, 5):
#     print j, ':', i.next(j)
# i.next(14)

# 13.13.4 *多类型定制
class Numstr(object):
    def __init__(self, num=0, str=''):
        self.num = num
        self.str = str

    def __str__(self):
        return '[%d::%r]' % (self.num, self.str)
    __repr__ = __str__

    def __add__(self, other):
        if isinstance(other, Numstr):
            return self.__class__(self.num+other.num, self.str+other.str)
        else:
            raise (TypeError, 'not a Numstr')

    def __mul__(self, other):
        if isinstance(other, Numstr):
            return self.__class__(self.num*other.num, self.str*other.num)
        else:
            raise (TypeError, 'not a Numstr')

    def __nonzero__(self):
        return self.num or len(self.str)

    def __cmp__(self, other):
        return True
        # cmp(self.num, other.num) + cmp(self.str, other.str)

# a = Numstr(3, 'lilang')
# b = Numstr(2, 'lilang2')
# c = Numstr(2, 'lilang2')
# print a*b, b==c

# 13.14 私有化 page544 __实现简单的私有化
# 13.15 *授权
# 13.15.1 包装 。你可以包装任何类型作为一个类的核心成员，以使新对象的行为模仿你想要的数据类型中已存在的行为，并且去掉你不希望存在的行为；
# 它可能会要做一些额外的事情
# 13.15.2 实现授权 实现授权的关键点就是覆盖__getattr__()方法

class WrapMe(object):
    def __init__(self,obj):
        self.__data = obj

    def get(self):
        return self.__data

    def __repr__(self):
        return 'sel.__data'

    def __str__(self):
        return str(self.__data)

    def __getattr__(self, attr):
        return getattr(self.__data, attr)

# a = WrapMe(3.4+4.2j)
# print a, a.real, a.imag, a.conjugate(), a.get()

# b = WrapMe([123, 'foo', 34.56])
# b.append(566)
# b.append(123)
# print b, b.index('foo'), b.count(123), b.pop(), b.get()[3]

class TimeWrapMe(object):
    def __init__(self, obj):
        self.__data = obj
        self.__ctime = self.__mtime = self.__atime = time()

    def get(self):
        self.__atime = time()
        return self.__data

    def gettimeval(self, t_type):
        if not isinstance(t_type, str) or t_type[0] not in 'cma':
            raise (TypeError, ' argument is error')
            return getattr(self, '_%s_%stime' % (self.__class__.__name__, t_type[0]))

    def gettimestr(self, t_type):
        return ctime(self.gettimeval(t_type))

    def set(self, obj):
        self.__data = obj
        self.__mtime = self.__atime = time()

    def __repr__(self):
        self.__atime = time()
        return 'self.__data'

    def __str__(self):
        self.__atime = time()
        return str(self.__data)

    def __getattr__(self, attr):
        self.__atime = time()
        return getattr(self.__data, attr)

# a = TimeWrapMe('932')
# a.gettimestr('c')
# print a, a.gettimestr('c'),a.gettimestr('m'), a.gettimestr('a'), a
# a
# print a.gettimestr('c'),a.gettimestr('m'), a.gettimestr('a')

# 13.16 新式类的高级特性
# 13.16.1 新式类的通用特性 553 ,各种散兵游勇
# 13.16.2 __slots__类属性

class SlottedClass(object):
    __slots__ = ('foo','bar')
# c = SlottedClass()
# print c
# c .foo =42
# print c, c.XXX

# 13.16.3 特殊方法__getattribute__()
# 13.16.4 描述符  类属性>数据描述符>实例属性>非数据描述符>默认为__getattr__() page558

class DevNull(object):
    def __init__(self, name=None):
        self.name = name

    def __get__(self, obj, typ = None):
        print ('gogogog[%s]' %self.name)

    def __set__(self, obj, val):
        print ('wtf[%s to %r]' %(self.name, val))

class C1(object):
    foo = DevNull()
#
# c1 = C1()
# print c1.foo
# c1.foo = 'bar'
# print c1.foo
# x = c1.foo
# c1.__dict__['foo'] = 'bar'
# x = c1.foo

class ProtectAndHideX(object):
    def __init__(self, x):
        assert isinstance(x, int), 'x must be an integer!'
        self.__x = ~x

    def get_x(self):
        return ~self.__x

    x = property(get_x)

# inst = ProtectAndHideX('foo')
# inst = ProtectAndHideX(10)
# print inst.x
# inst.x = 20

# 13.16.5 Metaclasses 和__metaclass__ y元类 page572
# 13.17 相关模块和文档


# 13.8 练习 page575
#13-1 :面向对象编程踩上了进化的步伐，增强了结构化编程，实现了数据与动作的融合：数据层和逻
# 辑层现在由一个可用以创建这些对象的简单抽象层来描述

if __name__ == '__main__':
    print ('hell')