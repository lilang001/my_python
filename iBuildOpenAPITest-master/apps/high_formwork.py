#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import requests.packages.urllib3.util.ssl_
from random import randint, choice
import os
dir_path = os.path.dirname(os.path.abspath(__file__ + "/../"))
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
import urllib3
urllib3.disable_warnings()


def __Generate_JSONV2_Items(deviceID):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now()
    item = {}
    # item['eigenvalue'] = randint(10, 300) / 10.0
    # item['status'] = randint(0, 1)
    """{
      "deviceId": "xxxxx",
      "deviceTime": "2018-04-28 13:25:01",
      "monitorVal": 45.9,
      "electricLevel": 5,
      "signalLevel": 4,
      "deviceType": 1,
      "handStatus": 1,
      "warningType": 1,
      "handTime": "2018-04-28 13:25:01"
    }
    """
    item['deviceid'] = deviceID
    item['deviceTime'] = Operation_time
    item['electricLevel'] = choice(range(5))
    item['signalLevel'] = choice(range(5))
    item['deviceType'] = choice(range(5))
    item['handStatus'] = choice(range(3))
    item['warningType'] = choice(range(2))
    item['handTime'] = Operation_time
    if now.hour <= 12:
        item['monitorVal'] = 100 + now.hour * randint(5, 9) / 10.0
    else:
        item['monitorVal'] = 100 - (now.hour - 12) * randint(5, 9) / 10.0

    return item


def JSONV2_Request(deviceID):
    # if Operation_time != '0':
    # Operation_time = Operation_time[:-3] + '0' + Operation_time[-2:]
    tmpreq = __Generate_JSONV2_Items(deviceID)

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(
        JSONV2_Request('Bing_high_formwork'), indent=4, ensure_ascii=False))
    # while 1>0:
# run()
# time.sleep(60)
