# -*- coding: utf-8 -*-
__author__ = 'admin'

import json
f = open('json_txt.txt', 'r')
json_txt = str(f.readlines())

def changejson(txt):
    txt = json.dumps(txt)
    txt = json.loads(txt)
    return txt

f.close()

if __name__ == '__main__':
    print changejson(json_txt)
