# -*- coding: utf-8 -*-
__author__ = 'Administrator'

import MySQLdb

conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='auto_testing', port=3306,charset='utf8')
cur = conn.cursor()
cur.execute('SELECT  * FROM auto_testing ')
a = cur.fetchall()
cur.close()

def update_output(output, id):
    update = conn.cursor()
    update.execute('update auto_testing SET actualoutput="{output}" WHERE id={id}'.format(output=output, id=id))
    conn.commit()
    print(update)
    update.close()


def result(id2):
    content = conn.cursor()
    content.execute('SELECT expectoutput,actualoutput FROM auto_testing WHERE id="{id2}"'.format(id2=id2))
    answer = content.fetchall()
    if answer[0][1] == answer[0][0]:
        content.execute('update auto_testing SET testresult=2 WHERE id="{id2}"'.format(id2=id2))
        conn.commit()
        return True
    else:
        content.execute('update auto_testing SET testresult=1 WHERE id="{id2}"'.format(id2=id2))
        conn.commit()
        return False
    content.close()

def fps_conn():
    conn1 = MySQLdb.Connect(host='192.168.1.142', user='root', passwd='1234', db='fps_1020', port=3306,charset='utf8')
    return conn1


