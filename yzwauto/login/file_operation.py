# -*- coding: utf-8 -*-
__author__ = 'admin'


def write_file(filename_new, my_list_new):
    f = open(filename_new, 'w')
    for i in my_list_new:
        for j in i:
            if isinstance(j,unicode) == True:
                f.write(j.encode('utf-8'))
            else:
                f.write(str(j))
            f.write(' ')
        f.write('\n')
    f.close()

# s = write_file('11lilang334',[('1',2,3),('2',3,4)])


