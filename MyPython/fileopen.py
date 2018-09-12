# -*- coding: utf-8 -*-
import sys
f = open('D:/test', 'wb')
a = '李朗111啊哈哈'
print a
f.write(a)
f.close()
fr = open('D:/test', 'rb').read()

print(fr)


