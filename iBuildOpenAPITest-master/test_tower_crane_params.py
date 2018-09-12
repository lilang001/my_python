#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from OpenAPI import OpenAPI
from config import elkSearch, pyMongodb, Check
import os, time
import HtmlTestRunner
from apps import tower_crane_params as tower_params
dir_path = os.path.dirname(os.path.realpath(__file__))


class tower(unittest.TestCase):
    def setUp(self):
        self.mongo = pyMongodb.pymongo()
        self.method = 'upload.towerCraneDeviceParams'

    def test_01(self):
        """推送正式设备数据"""
        data = tower_params.JSONV2_Request("tower")
        deviceId = data['deviceId']
        longitude = data['longitude']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkParams(longitude, self.method)

        mongoLog = self.mongo.getbyParams(longitude,
                                          "tower_crane_device_params")
        del mongoLog['editDate']

        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(deviceId, elkLog['deviceCode'])

    def test_02(self):
        """推送正式设备数据-无 deviceId 字段"""
        data = tower_params.JSONV2_Request("tower")
        longitude = data['longitude']
        del data['deviceId']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual("deviceId字段不能为空", elkLog['exceptionContent'])

    def test_03(self):
        """推送正式设备数据-推送未定义字段"""
        data = tower_params.JSONV2_Request("tower")
        longitude = data['longitude']
        data['pm110'] = 100
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual(1, elkLog['uploadStatus'])
        mongoLog = self.mongo.getbyParams(longitude,
                                          "tower_crane_device_params")
        del mongoLog['editDate']
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_04(self):
        """推送正式设备数据-字段类型不正确 double->string"""
        data = tower_params.JSONV2_Request("tower")
        data['longitude'] = "longitude-string"
        longitude = data['longitude']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual("longitude字段类型不正确", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_05(self):
        """推送正式设备数据-设备ID不存在"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = tower_params.JSONV2_Request("tower不存在")
        longitude = data['longitude']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual("未找到设备", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_06(self):
        """推送正式设备数据-设备未激活"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = tower_params.JSONV2_Request("tower-NotActive")
        longitude = data['longitude']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual("设备未激活", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_07(self):
        """推送正式设备数据-数据超长"""
        data = tower_params.JSONV2_Request("tower")
        longitude = data['longitude']
        data['override'] = 10000000000000000
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual("override字段类型不正确", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
    # env = tower()
    # env.setUp()
    # env.test_01()
    # env.test_07()
