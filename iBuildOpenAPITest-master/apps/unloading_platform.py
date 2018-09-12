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
        "deviceTime": Operation_time,
        "warning": __Generate_WarningType(),
        "loadWeight": randint(0, 30) / 10.0,
        "dipAngleX": randint(0, 10) / 10.0,
        "dipAngleY": randint(0, 10) / 10.0
    }

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request('sg001'), indent=4, ensure_ascii=False))
    # print(__Generate_WarningType())
    # while 1>0:
# run()
# time.sleep(60)
