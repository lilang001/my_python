#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
from random import randint, choice
import os
dir_path = os.path.dirname(os.path.abspath(__file__ + "/../"))


def JSONV2_Request(deviceID):
    Operation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tmpreq = {
        "deviceId": deviceID,
        "longitude": randint(0, 100000) / 10.0,
        "latitude": randint(0, 1000) / 10.0,
        "override": randint(0, 100),
        "minAmplitude": randint(0, 100) / 1.0,
        "maxAmplitude": randint(0, 100) / 1.0,
        "maxFourLiftingCapacity": randint(0, 100) / 1.0,
        "maxFourLiftingCapacityAmplitude": randint(0, 100) / 1.0,
        "maxFourAmplitude": randint(0, 100) / 1.0,
        "maxFourAmplitudeLiftingCapacity": randint(0, 100) / 1.0,
        "maxTwoLiftingCapacity": randint(0, 100) / 1.0,
        "maxTwoLiftingCapacityAmplitude": randint(0, 100) / 1.0,
        "maxTwoAmplitude": randint(0, 100) / 1.0,
        "maxTwoAmplitudeLiftingCapacity": randint(0, 100) / 1.0,
        "localX": randint(0, 100) / 1.0,
        "localY": randint(0, 100) / 1.0,
        "liftingArmLength": randint(0, 100) / 1.0,
        "balanceArmLength": randint(0, 100) / 1.0,
        "towerBodyHeight": randint(0, 100) / 1.0,
        "towerHeadHeight": randint(0, 100) / 1.0
    }

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request('sg001'), indent=4, ensure_ascii=False))
    # while 1>0:
# run()
# time.sleep(60)
