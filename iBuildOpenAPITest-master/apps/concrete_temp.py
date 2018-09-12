#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import requests.packages.urllib3.util.ssl_
from random import randint
import os
import urllib3
dir_path = os.path.dirname(os.path.abspath(__file__ + "/../"))
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
urllib3.disable_warnings()


def __Generate_JSONV2_Items(deviceID):
    now = datetime.datetime.now()
    item = {}
    # item['temp'] = randint(500, 1000) / 10.0
    # item['stress'] = randint(10, 99) / 10.0
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    item['deviceId'] = deviceID
    item['deviceTime'] = Operation_time
    if now.hour <= 12:
        item['temp'] = 20 + now.hour * randint(1, 9) / 10.0
        item['stress'] = 60 + now.hour * randint(5, 9) / 10.0
    else:
        item['temp'] = 20 - (now.hour - 12) * randint(1, 9) / 10.0
        item['stress'] = 60 - (now.hour - 12) * randint(5, 9) / 10.0

    return item


def JSONV2_Request(deviceID):
    req = __Generate_JSONV2_Items(deviceID)

    return req


if __name__ == "__main__":
    print(json.dumps(JSONV2_Request('sg001'), indent=4, ensure_ascii=False))
    # while 1>0:
