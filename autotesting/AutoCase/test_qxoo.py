__author__ = 'Administrator'
# -*- coding: utf-8 -*-
__author__ = 'qxoo'

class Driver(object):
    a = 20

    def open(self):
        print 'open'

    def close(self):
        print 'close'

class Driver2(Driver):
    a = 100

    def open(self):
        print 'open2'

    def close(self):
        print 'close2'

def p_log(DRIVER):
    a = DRIVER()
    def _func(func):
        def fwrap(*args, **kwargs):
            kwargs['driver'] = a
            a.open()
            func(*args, **kwargs)
            a.close()
        return fwrap
    return _func

@p_log(Driver2)
def testfunc(k, driver=None):
    print 'test'
    print driver.a
    print k


@p_log(Driver)
def testfunc1(name, age, driver=None):
    print name
    print age


if __name__ == '__main__':
    testfunc(18)