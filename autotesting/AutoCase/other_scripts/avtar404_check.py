# _*_ coding:utf-8 _*_
__author__ = 'Administrator'
import requests
import time
import sqls
import threading
from mysql import select, auto
import Queue
queue = Queue.Queue()
result = select(sqls.ava)
for row in result:
    queue.put(row)

def check_avatar(row):
    user_id = row[0]
    value1 = 'http://www.maiziedu.com/uploads/'+row[1]
    value2 = 'http://www.maiziedu.com/uploads/'+row[2]
    value3 = 'http://www.maiziedu.com/uploads/'+row[3]
    if requests.get(value1).status_code == 404:
        auto('INSERT INTO AutoTesting.avatar VALUES ("{user_id}", "404"),"{img}"'.format(user_id=user_id, img=row[1]))
    if requests.get(value2).status_code == 404:
        auto('INSERT INTO AutoTesting.avatar VALUES ("{user_id}",  "404"),"{img}"'.format(user_id=user_id, img=row[2]))
    if requests.get(value3).status_code == 404:
        auto('INSERT INTO AutoTesting.avatar VALUES ("{user_id}",  "404"),"{img}"'.format(user_id=user_id, img=row[3]))
    #time.sleep(1)
    print user_id

# if __name__ == '__main__':
#     check_avatar()

def _run():
    while 1:
        try:
            row = queue.get_nowait()
            check_avatar(row)
        except:
            return


ts = [threading.Thread(target=_run, name='threading1') for i in range(100)]
for t in ts:
    t.start()
t.join()