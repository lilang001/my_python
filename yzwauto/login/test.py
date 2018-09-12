# -*- coding: utf-8 -*-
__author__ = 'admin'

import Queue
import threading
import time
from login import sign_up, tender
from sql_con import select, sign_up_sql, tender_sql
queue = Queue.Queue()
f = open('user_bak.txt', 'r')
my_list = f.readlines()
TenderSysNo = 34807
sign_up_list = select(sign_up_sql.format(TenderSysNo=TenderSysNo))
tender_list = select(tender_sql.format(TenderSysNo=TenderSysNo))

for row in my_list:
    queue.put(row)

def _run():
    while 1:
        try:
            row = queue.get_nowait()
            row = row.split(' ')
            try:
                # 投标脚本
                if (int(row[3].replace('\n', '')),) in tender_list:
                    tender(row[0], row[1],  str(TenderSysNo), row[3])
                # 报名脚本
                # if (int(row[3].replace('\n', '')),) not in sign_up_list:
                #     sign_up(row[0], row[1], str(TenderSysNo), row[3])
                    print row[0],  'OK'
                else:
                    print row[0], 'PASS'

            except Exception as e:
                print row[0], 'error', e
        except Exception as e:
            print e
            return
ts = [threading.Thread(target=_run, name='threading1') for i in range(2)]
for t in ts:
    t.start()
    time.sleep(60)
t.join()