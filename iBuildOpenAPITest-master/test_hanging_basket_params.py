#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from OpenAPI import OpenAPI
from config import elkSearch, pyMongodb, Check
import os, time
import HtmlTestRunner
from OpenAPI import OpenAPI
from apps import hanging_basket_params as hang_params_data
dir_path = os.path.dirname(os.path.realpath(__file__))


class hanging_params(unittest.TestCase):
    def setUp(self):
        self.mongo = pyMongodb.pymongo()
        self.method = 'upload.hangingBasketDeviceParams'

    def test_01(self):
        """推送测试设备数据"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hang_params_data.JSONV2_Request("hanging")
        longitude = data['longitude']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkParams(longitude, self.method)

        mongoLog = self.mongo.getbyParams(longitude,
                                          "hanging_basket_device_params")
        if 'editDate' in mongoLog:
            del mongoLog['editDate']

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_02(self):
        """推送测试设备数据-推送未定义字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hang_params_data.JSONV2_Request("hanging")
        longitude = data['longitude']
        data['pm110'] = 100
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkParams(longitude, self.method)

        # mongoLog = self.mongo.getbyDeviceTime(longitude, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_03(self):
        """推送正式设备数据-字段类型不正确double->string"""
        data = hang_params_data.JSONV2_Request("hanging")
        data['latitude'] = "latitudeDoubleToString"
        longitude = data['longitude']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual("latitude字段类型不正确", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_04(self):
        """推送正式设备数据-设备ID不存在"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hang_params_data.JSONV2_Request("hang_params_data不存在")
        longitude = data['longitude']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual("未找到设备", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_05(self):
        """推送正式设备数据-设备未激活"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hang_params_data.JSONV2_Request("hanging-NotActive")
        longitude = data['longitude']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual("设备未激活", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_22(self):
        """推送正式设备数据-json 格式不正确"""
        data = hang_params_data.JSONV2_Request('hanging')
        longitude = data['longitude']
        data = json.dumps(data)
        data = data[:-1]
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkParams(longitude, self.method)
        self.assertEqual("json格式不正确", elkLog['exceptionContent'], elkLog)
        self.assertEqual(2, elkLog['uploadStatus'])


if __name__ == '__main__':

    unittest.main(verbosity=2)
    # t = hanging_params()
    # t.setUp()
    # t.test_01()
