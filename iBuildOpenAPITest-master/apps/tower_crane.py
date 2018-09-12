#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
from random import randint, choice
import os
from faker import Faker
dir_path = os.path.dirname(os.path.abspath(__file__ + "/../"))


def __Generate_tower_WarningType():
    #超重，风速
    a = choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3])
    #前后左右碰撞和碰撞报警
    b = choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 21, 22, 23])
    #左右限位
    c = choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 11])
    #内外限位
    d = choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 13])
    #上下限位
    e = choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 15])
    #区域保护
    f = choice([0, 0, 0, 0, 0, 0, 0, 0, 16, 17, 18, 19])
    #力矩
    g = choice([0, 0, 0, 0, 0, 0, 0, 0, 28])
    #倾斜
    h = choice([0, 0, 0, 0, 0, 0, 0, 0, 27])

    WType = str(bin(0)[2:].zfill(32))
    # if b > 0:
    #     WType = WType[:b] + str(1) + WType[b + 1:]
    #     WType = WType[:29] + str(1) + WType[30:]
    # if c > 0:
    #     WType = WType[:c] + str(1) + WType[c + 1:]
    # if d > 0:
    #     WType = WType[:d] + str(1) + WType[d + 1:]
    # if e > 0:
    #     WType = WType[:e] + str(1) + WType[e + 1:]
    # if f > 0:
    #     WType = WType[:f] + str(1) + WType[f + 1:]
    # if g > 0:
    #     WType = WType[:g] + str(1) + WType[g + 1:]
    # if h > 0:
    #     WType = WType[:h] + str(1) + WType[h + 1:]

    return WType


def JSONV2_Request(deviceID):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fake = Faker('zh_CN')
    tmpreq = {
        "deviceId": deviceID,
        "deviceTime": Operation_time,
        "warning": __Generate_tower_WarningType(),
        "liftingCapacity": randint(0, 10000) / 100.0,
        "safeLiftingCapacity": randint(0, 10000) / 100.0,
        "ratedMoment": randint(0, 10000) / 100.0,
        "amplitude": randint(0, 10000) / 100.0,
        "round": randint(0, 36000) / 100.0,
        "height": randint(0, 50000) / 100.0,
        "dipAngleX": randint(0, 36000) / 100.0,
        "dipAngleY": randint(0, 36000) / 100.0,
        "windSpeed": randint(0, 1000) / 100.0,
        "driverId": fake.ssn(),
        "driverName": fake.name()
    }

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request('sg001'), indent=4, ensure_ascii=False))
    # while 1>0:
# run()
# time.sleep(60)
