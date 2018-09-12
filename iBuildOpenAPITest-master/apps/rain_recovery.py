#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import requests
from random import randint, choice
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
import os
dir_path = os.path.dirname(os.path.abspath(__file__ + "/../"))
import urllib3
urllib3.disable_warnings()


def __Generate_JSON_Items():
    i = choice([5, 8])
    items = []
    while i > 0:
        itemIn = {}
        itemIn['groupName'] = u"房间 " + str(i)
        itemIn['inTemp'] = str(randint(-200, 450) / 10.0)
        itemIn['inHumidity'] = str(randint(0, 100) / 1.0)
        items.append(itemIn)
        i -= 1

    return items


def JSONV2_Request(deviceID):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tmpreq = {
        "deviceId": deviceID,
        "deviceTime": Operation_time,
        "waterLevel": randint(0, 2000) / 10.0,
        "autoWater": choice([True, False]),
        "timeStart": choice([True, False]),
        "outTemp": randint(-200, 450) / 1.0,
        "outHumidity": randint(0, 100) / 1.0,
        "groupList": __Generate_JSON_Items()
    }

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request('sg001'), indent=4, ensure_ascii=False))
    # while 1>0:
# run()
# time.sleep(60)
