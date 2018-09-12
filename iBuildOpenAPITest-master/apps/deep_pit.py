#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import requests.packages.urllib3.util.ssl_
from random import randint
import os
dir_path = os.path.dirname(os.path.abspath(__file__ + "/../"))
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
import urllib3
urllib3.disable_warnings()


def __Generate_JSONV2_Items(deviceID):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    now = datetime.datetime.now()
    items = []
    item = {}
    # item['current_test_value'] = randint(190, 300) / 10.0
    # item['single_change_value'] = randint(190, 300) / 10.0
    # item['cumulative_change_value'] = randint(190, 300) / 10.0
    # item['change_rate'] = randint(190, 300) / 10.0
    """
    {
      "deviceId": "xxxxx",
      "dateTime": "2018-04-28 13:25:01",
      "monitorVal": 13.0384,
      "xChangeValue": 13.0384,
      "yChangeValue": 13.0384,
      "xCumulativeChangeValue": 13.0384,
      "yCumulativeChangeValue": 13.0384,
      "deviceType": 1,
      "monitorType":1,
      "status": 0,
      "currentTestValue": 13.0384,
      "singleChangeValue": 13.0384,
      "cumulativeChangeValue": 13.0384,
      "changeRate": 13.0384
    }
    """
    item['deviceId'] = deviceID
    item['deviceTime'] = Operation_time
    if now.hour <= 12:
        item['current_test_value'] = 100 + now.hour * randint(5, 9) / 10.0
        item['single_change_value'] = 100 + now.hour * randint(5, 9) / 10.0
        item['cumulative_change_value'] = 100 + now.hour * randint(5, 9) / 10.0
        item['change_rate'] = 10 + now.hour * randint(1, 9) / 10.0
    else:
        item['current_test_value'] = 100 - (now.hour - 12) * randint(5,
                                                                     9) / 10.0
        item['single_change_value'] = 100 - (now.hour - 12) * randint(5,
                                                                      9) / 10.0
        item['cumulative_change_value'] = 100 + (now.hour - 12) * randint(
            5, 9) / 10.0
        item['change_rate'] = 10 + (now.hour - 12) * randint(1, 9) / 10.0
    item['status'] = 0

    items.append(item)
    return items


def JSONV2_Request(deviceID):
    req = __Generate_JSONV2_Items(deviceID)

    return req


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request('sg001'), indent=4, ensure_ascii=False))
    # while 1>0:
# run()
# time.sleep(60)
