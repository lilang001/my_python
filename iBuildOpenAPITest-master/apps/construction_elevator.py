#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import requests
from random import randint, choice
from faker import Faker
import os
dir_path = os.path.dirname(os.path.abspath(__file__ + "/../"))
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
import urllib3
urllib3.disable_warnings()


def __Generate_elevator_WarningType():
    #重量报警、预警
    a = choice([0, 0, 0, 0, 0, 1, 2, 3])
    # a = choice([0,0,0,0,0,0,0,0,0,0,1,2,3])
    #顶层报警、预警
    b = choice([0, 0, 0, 0, 0, 1, 2, 3])
    # 门打开，蹲底
    c = choice([0, 0, 0, 0, 0, 1, 2, 3])
    #风速报警、预警
    d = choice([0, 0, 0, 0, 0, 1, 2, 3])
    #防坠预警，人数报警
    e = choice([0, 0, 0, 0, 0, 1, 2, 3])

    WType = str(bin(0)[2:].zfill(32))
    """
    if b > 0:
        WType = WType[:12] + str(bin(b)[2:].zfill(2)) + WType[14:]
    if c > 0:
        WType = WType[:10] + str(bin(c)[2:].zfill(2)) + WType[12:]
    if d > 0:
        WType = WType[:8] + str(bin(d)[2:].zfill(2)) + WType[10:]
    if e > 0:
        WType = WType[:6] + str(bin(e)[2:].zfill(2)) + WType[8:]
    """

    return WType


def JSONV2_Request(deviceID):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fake = Faker()
    floor = randint(-10, 200)
    if floor == 0:
        floor = 1
    tmpreq = {
        "deviceId": deviceID,
        "deviceTime": Operation_time,
        "warning": __Generate_elevator_WarningType(),
        "currentLoad": str(randint(0, 500) / 100.0),
        "currentRatedLoad": randint(0, 500) / 100.0,
        "personCount": randint(0, 30),
        "floor": floor,
        "speed": randint(0, 500) / 100.0,
        "windSpeed": randint(0, 8) / 1.0,
        "height": randint(0, 1000) / 10.0,
        "driverId": fake.ssn(),
        "driverName": "张三",
        "windScale": randint(0, 5),
        "dipAngleX": randint(0, 30) / 10.0,
        "dipAngleY": randint(0, 30) / 10.0
    }

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request('sg001'), indent=4, ensure_ascii=False))
    # while 1>0:
# run()
# time.sleep(60)
