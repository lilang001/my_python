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


def JSONV2_Request(deviceID):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tmpreq = {
        "deviceId": deviceID,
        "deviceTime": Operation_time,
        "pm25": randint(0, 999) / 10.0,
        "pm10": randint(0, 999) / 10.0,
        "tsp": randint(0, 99999) / 10.0,
        "noise": randint(0, 900) / 10.0,
        "windDirect": randint(0, 900) / 10.0,
        "windSpeed": randint(0, 900) / 10.0,
        "temp": randint(-300, 700) / 10.0,
        "humid": randint(0, 900) / 10.0,
        "atoms": randint(0, 20) / 10.0
    }

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request('sg001'), indent=4, ensure_ascii=False))
    # while 1>0:
# run()
# time.sleep(60)
