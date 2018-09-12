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


def JSONV2_Request(deviceID):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    w = choice([0, 0, 0, 0, 0, 1, 2, 3])
    WType = str(bin(w)[2:].zfill(8))

    tmpreq = {
        "deviceId": deviceID,
        "deviceTime": Operation_time,
        "warning": WType,
        "batteryVoltage": randint(0, 5) / 1.0,
        "temp": randint(1, 10000) / 100.0
    }

    return tmpreq


if __name__ == "__main__":
    print(json.dumps(JSONV2_Request('YG001'), indent=4, ensure_ascii=False))
