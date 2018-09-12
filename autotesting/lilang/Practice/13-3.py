# -*- coding: utf-8 -*-
__author__ = 'admin'



class MoneyFmt(object):
    __doc__ = u""" 对类进行定制。写一个类，用来将浮点数值转换为金额。在本练习里，我们使用美国
货币，但读者也可以自选任意货币。
基本任务: 编写一个dollarize()函数，它以一个浮点数值作为输入，返回一个字符串形式的
金额数。比如说：
dollarize(1234567.8901) ==> ‘$1,234,567.89.
dollarize()返回的金额数里应该允许有逗号(比如1,000,000)，和美元的货币符号。如果有负
号，它必须出现在美元符号的左边。完成这项工作后，你就可以把它转换成一个有用的类，名为
MoneyFmt。
MoneyFmt 类里只有一个数据值(即，金额)，和五个方法(你可以随意编写其他方法)。__init__()
构造器对数据进行初始化，update()方法把数据值替换成一个新值，__nonzero__()是布尔型的，当
数据值非零时返回True，__repr__()方法以浮点数的形式返回金额；而__str__()方法采用和
dollarize()一样的字符格式显示该值。
(a) 编写update()方法，以实现数据值的修改功能。
(b) 以你已经编写的 dollarize()的代码为基础，编写__str__()方法的代码
(c) 纠正__nonzero__()方法中的错误，这个错误认为所有小于1 的数值，例如，50 美分($0.50)，
返回假值(False)。
(d) 附加题: 允许用户通过一个可选参数指定是把负数数值显示在一对尖括号里还是显示一个
负号。默认参数是使用标准的负号。
    """

    def __init__(self, fl, flag='-'):
        assert isinstance(fl, float), 'fl must be a float'
        self.fl = float(fl)
        self.flag = flag

    def dollarize(self):
        val = round(self.fl, 2)
        strval = str(abs(val))
        pos = strval.find('.')
        while pos-3 > 0:
            strval = strval[:pos-3]+','+strval[pos-3:]
            pos -= 3
        if self.fl > 0:
            return '$'+strval
        elif self.flag == '-':
            return '-'+'$'+strval
        else:
            return '['+'$'+strval+']'

    def update(self, val):
        self.fl = val

    def __nonzero__(self):
        if abs(self.fl) < 1:
            return False
        else:
            return True

    def __str__(self):
        return self.dollarize()

    def __repr__(self):
        return repr(self.fl)


f1 = MoneyFmt(-22222222221.1, '-')
print f1, bool(f1)
f1.update(2222344.1)
print f1
