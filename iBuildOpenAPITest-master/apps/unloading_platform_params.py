#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import requests
from random import randint
import os
dir_path = os.path.dirname(os.path.abspath(__file__ + "/../"))
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
import urllib3
urllib3.disable_warnings()


def __Generate_WarningType():
    a = randint(0, 15)
    WType = str(bin(a)[2:].zfill(8))

    return WType


def JSONV2_Request(deviceID):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tmpreq = {
        "deviceId": deviceID,
        "longitude": randint(0, 100000) / 10.0,
        "latitude": randint(0, 1000) / 10.0,
        "stdLoadWeight": randint(0, 100) / 1.0,
        "minDipAngleX": randint(0, 100) / 1.0,
        "maxDipAngleY": randint(0, 100) / 1.0,
        "earlyWarningCoefficient": randint(0, 100) / 1.0,
        "warningCoefficient": randint(0, 100) / 1.0,
        "earlyWarningDipAngle": randint(0, 100) / 1.0,
        "warningDipAngle": randint(0, 100) / 1.0
    }

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request('sg001'), indent=4, ensure_ascii=False))
    # print(__Generate_WarningType())
    # while 1>0:
# run()
# time.sleep(60)
