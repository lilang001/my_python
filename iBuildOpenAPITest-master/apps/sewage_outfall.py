#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


def __Generate_JSONV2_Items():
    items = []
    item = {}
    item['temp'] = randint(-100, 200) / 10.0
    item['ph_value'] = randint(0, 140) / 10.0

    items.append(item)
    return items


def JSONV2_Request(deviceID):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tmpreq = {
        "deviceId": deviceID,
        "deviceTime": Operation_time,
        "temp": randint(-100, 200) / 10.0,
        "phValue": randint(0, 140) / 10.0
    }

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request('ws001'), indent=4, ensure_ascii=False))
    # while 1>0:
# run()
# time.sleep(60)
