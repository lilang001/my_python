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


def __Generate_JSONV2_Items(deviceID):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item = {}

    item['deviceId'] = deviceID
    item['deviceTime'] = Operation_time
    item['currentCounterWeight'] = randint(0, 500) / 1.0
    item['currentLoadWeight'] = randint(0, 500) / 1.0
    item['waver'] = randint(0, 10) / 1.0
    item['swingAngle'] = randint(0, 10) / 1.0
    item['currentHeight'] = randint(0, 50) / 1.0
    item['personCount'] = randint(0, 15)
    item['buckleCount'] = randint(0, 15)
    item['groupList'] = []
    i = choice([1, 2, 3, 4])
    while i > 0:
        itemIn = {}
        itemIn['wireState'] = choice(["01", "02"])
        item['groupList'].append(itemIn)
        i -= 1
    return item


def JSONV2_Request(deviceID):
    tmpreq = __Generate_JSONV2_Items(deviceID)

    return tmpreq


if __name__ == "__main__":
    print(json.dumps(JSONV2_Request('sg001'), indent=4, ensure_ascii=False))
