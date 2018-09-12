#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import log
import requests.packages.urllib3.util.ssl_
from random import randint, choice
import os
dir_path = os.path.dirname(os.path.abspath(__file__ + "/../"))
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
import urllib3
urllib3.disable_warnings()


def __Generate_JSONV2_Items(vehicleNumber, entryOrExit, regiteredVehicle,
                            deviceID):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item = {}
    item['deviceId'] = deviceID
    item['deviceTime'] = Operation_time
    item['vehicleNumber'] = vehicleNumber
    item['entryOrExit'] = entryOrExit
    item['entryOrExitTime'] = Operation_time
    item['registeredVehicle'] = regiteredVehicle
    return item


def JSONV2_Request(deviceID=''):

    req = {"list": []}

    x = ["1", "2", "3", "4"]
    vehicleNumber = "川A" + choice(x) + choice(x) + choice(x) + choice(x)
    # vehicleNumber = unicode(vehicleNumber_x, 'utf-8')
    # print vehicleNumber
    """
    vehicleNumber_List = log.get_vehicleNumber(ENV, ProjectSysNo,
                                               vehicleNumber)
    # print vehicleNumber_List

    if len(vehicleNumber_List) == 0:
        entryOrExit = 0
        regiteredVehicle = choice([True, False])
    else:
        entryOrExit_x = vehicleNumber_List['entryOrExit']
        if entryOrExit_x == 0:
            entryOrExit = 1
        else:
            entryOrExit = 0
        regiteredVehicle = vehicleNumber_List['regiteredVehicle']
    # print vehicleNumber,entryOrExit,regiteredVehicle

    log.log_vehicleNumber(ENV, ProjectSysNo, vehicleNumber, entryOrExit,
                          regiteredVehicle)
    """
    req = __Generate_JSONV2_Items(vehicleNumber,
                                  randint(0, 1),
                                  choice([True, False]), deviceID)

    return req


if __name__ == "__main__":

    print(json.dumps(
        JSONV2_Request("QA", "10079", 'test001'), indent=4,
        ensure_ascii=False))
