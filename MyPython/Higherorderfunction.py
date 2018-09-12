__author__ = 'Administrator'
from functools import reduce
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# f = abs
# print(f(-10))

# def add(x, y, z):
#     return z(x) + z(y)
#
# x = 100
# y = -15
# z = abs
# print(add(x, y, z))
#
# def f(x):
#     return x*x
#
# def d(d1, d2):
#     return d1 + d2
# print(reduce(d, [1, 2, 3, 4, 5]))
#
# def s(x1, y1):
#     return x1*y1
#
# l = reduce(s, [1, 2, 3, 4, 5])
# print(l)
#
# def larger(x):
#     if x > 10:
#         return 100
#
# r0 = list(filter(larger,{1,100,140}))
# print(r0)

def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

@log
def now():
    print('李朗')

print(now())



