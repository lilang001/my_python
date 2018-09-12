#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from OpenAPI import OpenAPI
from config import elkSearch, pyMongodb, Check
import os, time
import HtmlTestRunner
from apps import construction_elevator_params as construction
dir_path = os.path.dirname(os.path.realpath(__file__))


class construction_params(unittest.TestCase):
    def setUp(self):
        self.mongo = pyMongodb.pymongo()
        self.method = 'upload.constructionElevatorDeviceParams'

    def test_01(self):
        "推送正式设备数据"
        data = construction.JSONV2_Request("construction")
        longitude = data['longitude']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], res.json())

        elkLog = elkSearch.elkParams(longitude, self.method)

        mongoLog = self.mongo.getbyParams(
            longitude, "construction_elevator_device_params")
        del mongoLog['editDate']

        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")

    def test_04(self):
        "推送正式设备数据-推送未定义字段"
        data = construction.JSONV2_Request("construction")
        longitude = data['longitude']
        data['pm110'] = 100
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual(1, elkLog['uploadStatus'])
        mongoLog = self.mongo.getbyParams(
            longitude, "construction_elevator_device_params")
        del mongoLog['editDate']

        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_06(self):
        "推送正式设备数据-字段类型不正确 double->string"
        data = construction.JSONV2_Request("construction")
        data['ratedLoad'] = "longitude-string"
        longitude = data['longitude']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual("ratedLoad字段类型不正确", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_07(self):
        "推送正式设备数据-设备ID不存在"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = construction.JSONV2_Request("construction不存在")
        longitude = data['longitude']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual("未找到设备", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_08(self):
        "推送正式设备数据-设备未激活"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = construction.JSONV2_Request("construction-NotActive")
        longitude = data['longitude']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual("设备未激活", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_22(self):
        """推送正式设备数据-json 格式不正确"""
        data = construction.JSONV2_Request('construction')
        longitude = data['longitude']
        data = json.dumps(data)
        data = data[:-10]
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual("json格式不正确", elkLog['exceptionContent'], elkLog)
        self.assertEqual(2, elkLog['uploadStatus'])

    """
    def test_11(self):
        "推送正式设备数据-数据超长"
        data = construction.JSONV2_Request("construction")
        longitude = data['longitude']
        data['earlyWarningCoefficient'] = 10000000000000000
        deviceId = data['deviceId']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(longitude)
        self.assertEqual("earlyWarningCoefficient 字段超长",
                         elkLog['exceptionContent'])
        self.assertEqual(deviceId, elkLog['deviceCode'])
        self.assertEqual(2, elkLog['uploadStatus'])
    """


if __name__ == '__main__':
    unittest.main(verbosity=2)
    # env = construction_params()
    # env.setUp()
    # env.test_01()
