# -*- coding: utf-8 -*-
__author__ = 'admin'
def foo():
    return True

def bar():
    "bar() does not do much"
    return True

foo.__doc__ = 'foo() does not do much'
foo.tester = '''
if foo():
    print ('PASSED')
else:
    print ('FailED')
'''

for eachAttr in dir():
    obj = eval(eachAttr)
    if isinstance(obj, type(foo)):
        if hasattr(obj,'__doc__'):
            print ('\nFunction "%s" has a doc string:\n\t%s'%(eachAttr,obj.__doc__))
            if hasattr(obj,'tester'):
                print ('Fucntion "%s" has a tester ..'%eachAttr)
                exec(obj.tester)
            else:
                print ('Fucntion "%s" has no tester ..'%eachAttr)
    else:
        print('"%s" is not a function'%eachAttr)
if __name__=='__main':
   print ('a')