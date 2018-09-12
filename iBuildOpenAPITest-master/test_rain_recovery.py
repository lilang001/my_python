#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from OpenAPI import OpenAPI
from config import elkSearch, pyMongodb, Check
import os, time
import HtmlTestRunner
from apps import rain_recovery as rain_data
dir_path = os.path.dirname(os.path.realpath(__file__))


class rain_recovery(unittest.TestCase):
    def setUp(self):
        self.mongo = pyMongodb.pymongo()
        self.method = 'upload.rainRecoveryLiveData'
        self.NdeviceId = 'rain'

    def test_01(self):
        "推送测试设备数据"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = rain_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)

        mongoLog = self.mongo.getbyDeviceTime(deviceTime, "rain_recovery")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_02(self):
        "推送测试设备数据-无deviceTime字段"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = rain_data.JSONV2_Request(self.NdeviceId)
        del data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        # elkLog = elkSearch.elkDevice(deviceTime, self.method)

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "rain_recovery")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

    def test_03(self):
        "推送测试设备数据-无outTemp字段"
        data = rain_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data["outTemp"]
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        # self.assertEqual("outTemp字段不能为空", elkLog['exceptionContent'])

        mongoLog = self.mongo.getbyDeviceTime(deviceTime, "rain_recovery")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    """
    def test_04(self):
        "推送测试设备数据-无waterLevel字段"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = rain_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['waterLevel']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("waterLevel字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "rain_recovery")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_05(self):
        "推送测试设备数据-无autoWater字段"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = rain_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['autoWater']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("autoWater字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "rain_recovery")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_06(self):
        "推送测试设备数据-无timeStart字段"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = rain_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['timeStart']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("timeStart字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "rain_recovery")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_07(self):
        "推送测试设备数据-无groupList字段"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = rain_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['groupList']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("groupList字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "rain_recovery")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])
    """

    def test_08(self):
        "推送测试设备数据-无groupName字段"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = rain_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['groupList'][0]['groupName']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("groupName字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "rain_recovery")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_09(self):
        "推送测试设备数据-推送未定义字段"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = rain_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data['pm110'] = 100
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "rain_recovery")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_010(self):
        "推送正式设备数据-字段类型不正确double->string"
        data = rain_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data['outTemp'] = "string"
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("outTemp字段类型不正确", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_011(self):
        "推送正式设备数据-字段类型不正确 datetime->string"
        data = rain_data.JSONV2_Request(self.NdeviceId)
        data['deviceTime'] = "deviceTime-string"
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("deviceTime字段类型不正确", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_012(self):
        "推送正式设备数据-设备ID不存在"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = rain_data.JSONV2_Request("rain-NotExist")
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("未找到设备", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_013(self):
        "推送正式设备数据-设备未激活"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = rain_data.JSONV2_Request("rain-NotActive")
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("设备未激活", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_22(self):
        """推送正式设备数据-json 格式不正确"""
        data = rain_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        data = data[:-1]
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("json格式不正确", elkLog['exceptionContent'], elkLog)
        self.assertEqual(2, elkLog['uploadStatus'])


if __name__ == '__main__':

    # unittest.main(verbosity=2)
    t = rain_recovery()
    t.setUp()
    t.test_013()
