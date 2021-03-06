#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import requests
from random import randint, choice
import os
dir_path = os.path.dirname(os.path.abspath(__file__ + "/../"))
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
import urllib3
urllib3.disable_warnings()


def JSONV2_Request(deviceID):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    floor = randint(-10, 200)
    if floor == 0:
        floor = 1
    tmpreq = {
        "deviceId": deviceID,
        "longitude": randint(0, 100000) / 10.0,
        "latitude": randint(0, 1000) / 10.0,
        "stdLoadWeight": randint(200, 300) / 1.0,
        "stdCounterWeight": randint(0, 3) / 1.0,
        "errorCounterWeight": randint(0, 3) / 1.0,
        "maxWaver": randint(0, 10) / 10.0,
        "maxSwingAngle": randint(0, 10) / 10.0,
        "maxPersonCount": randint(5, 10),
        "minTopHeight": randint(1, 5) / 1.0
    }

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request('sg001'), indent=4, ensure_ascii=False))
    # while 1>0:
# run()
# time.sleep(60)
