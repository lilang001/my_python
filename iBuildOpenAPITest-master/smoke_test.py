#!/usr/bin/env python
# -*- coding: utf-8 -*-

from OpenAPI import OpenAPI
import json
import time, uuid
from datetime import datetime
from config import elkSearch


def test_Device_smoke():
    """硬件冒烟"""
    # mongo = pyMongodb.pymongo()
    deviceTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "temp": -4.0,
        "pm10": 43.9,
        "humid": 3.6,
        "deviceTime": deviceTime,
        "deviceId": "OPENAPI",
        "atoms": 1.6,
        "tsp": 3915.4,
        "pm25": 76.1,
        "noise": 33.9,
        "windSpeed": 12.2,
        "windDirect": 79.6
    }

    data = json.dumps(data)
    print(json.dumps(json.loads(data), indent=2, ensure_ascii=False))
    res = OpenAPI(method='upload.envMonitorLiveData', data=data)
    print(res)
    print(json.dumps(res.json(), indent=2, ensure_ascii=False))

    time.sleep(5.5)
    elkLog = elkSearch.elkDevice(deviceTime)
    print("\nelkLog:")
    print(json.dumps(elkLog))
    """
    time.sleep(1.5)
    mongoLog = mongo.getbyDeviceTime(deviceTime, "env_monitor")
    print("\nmongoLog:")
    print(mongoLog)

    Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
        mongoLog, elkLog, json.loads(data))
    print(Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match)
    """


def test_SoftWare_smoke():
    """软件冒烟"""
    # mongo = pyMongodb.pymongo()
    sourceID = str(uuid.uuid4())
    deviceTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = """
    {
        "sourceId": "874d33ec-190e-4814-b65b-0b4694c494dd",
        "actualStartTime":  "2017-12-14
        00:00:00",
        "planStartTime": "2017-12-14 00:00:00",
        "parentSourceId":  "874d33ec-190e-4814-b65b-0b4694c494dd",
        "sortIndex": 20,
        "completionRate": 0,
        "type": 1,
        "type1": 1,
        "projectSysNo": 10218,
        "partitioningName": "AutoTest-partitioningName2018-07-26 20:26:45",
        "name": "AutoTestName2018-07-26 20:26:45",
        "partitioningId":   "874d33ec-190e-4814-b65b-0b4694c494dd",
        "actualEndTime": "2018-05-26 00:00:00",
        "planEndTime": "2018-05-25 00:00:00",
        "status": 1
    }
    """

    # data = json.dumps(data)
    # print(sourceID)
    res = OpenAPI(method='upload.processTaskData', data=data)
    # print(json.dumps(res.json(), indent=2, ensure_ascii=False))

    time.sleep(3.5)
    elkLog = elkSearch.elkSoftware(sourceID)
    # print(json.dumps(elkLog))
    """
    time.sleep(1.5)
    mongoLog = mongo.getbySourceId(sourceID, "process_task")
    # print(mongoLog)

    # print(json.dumps(json.loads(data), indent=2, ensure_ascii=False))
    Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
        mongoLog, elkLog, json.loads(data))
    print(Mongo_ELK_Match, Mongo_ReqData_Match)
    """


if __name__ == "__main__":
    test_Device_smoke()
    # test_SoftWare_smoke()
