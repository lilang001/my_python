#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
import os
import uuid
import time
from OpenAPI import OpenAPI
from datetime import datetime
import HtmlTestRunner
from config import elkSearch, pyMongodb, Check
dir_path = os.path.dirname(os.path.realpath(__file__))


class OpenAPISign(unittest.TestCase):
    def test_SoftWare_smoke(self):
        """软件冒烟"""
        mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        sourceID = str(uuid.uuid4())
        deviceTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "sourceId": sourceID,
            "actualStartTime": deviceTime,
            "planStartTime": "2017-12-14 00:00:00",
            "parentSourceId": str(uuid.uuid4()),
            "sortIndex": 20,
            "completionRate": 0,
            "type": 1,
            "type1": 1,
            "projectSysNo": 10218,
            "partitioningName": "AutoTest-partitioningName2018-07-26 20:26:45",
            "name": "AutoTestName2018-07-26 20:26:45",
            "partitioningId": str(uuid.uuid4()),
            "actualEndTime": "2018-05-26 00:00:00",
            "planEndTime": "2018-05-25 00:00:00",
            "status": 1
        }

        data = json.dumps(data)
        # print(sourceID)
        res = OpenAPI(method='upload.processTaskData', data=data)
        # print(json.dumps(res.json(), indent=2, ensure_ascii=False))

        time.sleep(3.5)
        elkLog = elkSearch.elkSoftware(sourceID)
        # print(elkLog)

        time.sleep(1.5)
        mongoLog = mongo.getbySourceId(sourceID, "process_task")
        # print(mongoLog)

        # print(json.dumps(json.loads(data), indent=2, ensure_ascii=False))
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        print(Mongo_ELK_Match, Mongo_ReqData_Match)
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")

    def test_Device_smoke(self):
        """硬件冒烟"""
        mongo = pyMongodb.pymongo('172.16.0.137', 20200)
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
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))

        time.sleep(3.5)
        elkLog = elkSearch.elkDevice(deviceTime)
        # print("\nelkLog:")
        # print(json.dumps(elkLog))

        time.sleep(1.5)
        mongoLog = mongo.getbyDeviceTime(deviceTime, "env_monitor")
        # print("\nmongoLog:")
        # print(mongoLog)

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongoLog, elkLog, json.loads(data))
        print(Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match)
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")


if __name__ == '__main__':
    unittest.main(verbosity=2)
    # elk = elkSearch.elk()
    # res = elk.elkSearch(1, "2018-07-27 12:18:35")
    # print(res)

    # O = OpenAPISign()
    # O.test_Device_smoke()
