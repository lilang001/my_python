# -*- coding: utf-8 -*-
__author__ = 'admin'
import sys

# def foo():
#     print "\ncalling foo()..."
#     bar = 200
#     print "in foo(), bar is", bar
# bar = 100
# print "in __main__, bar is", bar
# foo()

# def foo():
#     pass
#
# foo.version = 0.2
# foo.__doc__ = '5555'
# print foo.version, foo.__doc__ , mymodule.version
class MyStorageDevice(object):
    pass

bag = MyStorageDevice()
bag.x = 100
bag.y = 200
bag.version = 0.1
bag.completed = False

print (bag.x)