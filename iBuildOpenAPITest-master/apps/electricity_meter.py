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


def JSONV2_Request(deviceID, usingCount=0):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tmpreq = {
        "deviceId": deviceID,
        "deviceTime": Operation_time,
        "usingCount": usingCount + randint(1, 5) / 1.0
    }

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request('sg001', 1), indent=4, ensure_ascii=False))
    # while 1>0:
# run()
# time.sleep(60)
