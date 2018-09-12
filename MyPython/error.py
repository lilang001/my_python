__author__ = 'Administrator'
import logging
def foo():
    r = sum()
    if r == (-1):
        return (-1)
    # do something
    return r

def bar():
    r = foo()
    if r == (-1):
        print('Error')
    else:
        pass


try:
    print('try...')
    r = 10 / 1
    print('result:', r)
except ZeroDivisionError as e:
    print('exception', e)
finally:
    print ('finally..')
print('end')



# err.py:
# def foo(s):
#     return 10 / int(s)
# def bar(s):
#     return foo(s) * 2
#
# def main():
#     try:
#         bar('0')
#     except Exception as e:
#         logging.exception(e)
# main()
# print('END')

# def foo(s):
#     n = int(s)
#     assert n != 0, 'n is zero!'
#     return 10 / n
#
# def main():
#     foo('0')
# main()

# import logging
# logging.basicConfig(level=logging.INFO)
# s = '0'
# n = int(s)
# logging.info('n = %d' % n)
# print(10 / n)
