# _*_ coding:utf8 _*_
__author__ = 'Administrator'

def test():
    a = 1
    b = a
    print (id(a), id(b))
    a = 2
    print (id(a), id(b))
    b = 3
    print (id(a), id(b))
    a = b
    print (id(a), id(b))


def foo():
    """This is a doc string."""
    return True

if __name__ == '__main__':
    print (test())




