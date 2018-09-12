#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'admin'

import Queue
import threading
from BidByAPI_Quo import SignUP_mainSingleUser, Bid_mainSingleUser, QA, PRD, PRDTest, PRE,  SigntenderFile_mainSingleUser, ViewCalibration_mainSingleUser

queue     = Queue.Queue()
userlist  = open('user.txt', 'r')
my_list   = userlist.readlines()
UserCount = 197
for row in my_list[:UserCount]:
    queue.put(row)

# 环境：QA , PRD, PRDTest, PRE
site        = PRD
# 招标 SysNo
TenderID    = 1100389
# 线程数
ThreadCount = 20
# 操作
# step =


def _run():
    while 1:
        try:
            row = queue.get_nowait()
            row = row.split(',')
            try:
                # SignUP_mainSingleUser(row[0],          row[1],  site,  TenderID)
                SigntenderFile_mainSingleUser(row[0],  row[1],  site,  TenderID)
                # Bid_mainSingleUser(row[0],             row[1],  site,  TenderID)
                #ViewCalibration_mainSingleUser(row[0],   row[1],  site,  TenderID)
            except Exception as ee:
                print(ee)
                print(row[0], 'error')
        except Exception as e:
            print(e)
            return


ts = [threading.Thread(target=_run, name='threading1') for i in range(ThreadCount)]
for t in ts:
    t.start()
t.join()
