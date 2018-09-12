#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from OpenAPI import OpenAPI
from config import elkSearch, pyMongodb, Check
import os, time
import HtmlTestRunner
from OpenAPI import OpenAPI
from apps import soil_temp as soil_data
dir_path = os.path.dirname(os.path.realpath(__file__))


class soil_temp(unittest.TestCase):
    def setUp(self):
        self.mongo = pyMongodb.pymongo()
        self.method = 'upload.curingRoomLiveData'
        self.NdeviceId = 'soil'

    def test_01(self):
        """推送测试设备数据"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = soil_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)

        mongoLog = self.mongo.getbyDeviceTime(deviceTime, "soil_temp")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_02(self):
        """推送测试设备数据-无deviceTime字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = soil_data.JSONV2_Request(self.NdeviceId)
        del data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        # elkLog = elkSearch.elkDevice(deviceTime, self.method)

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "soil_temp")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

    def test_03(self):
        """推送测试设备数据-无temp字段"""
        data = soil_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data["temp"]
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("temp字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "soil_temp")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_04(self):
        """推送测试设备数据-无humid字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = soil_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['humid']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("humid字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "soil_temp")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_05(self):
        """推送测试设备数据-推送未定义字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = soil_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data['pm110'] = 100
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "soil_temp")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_06(self):
        """推送正式设备数据-字段类型不正确double->string"""
        data = soil_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data['humid'] = "string"
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("humid字段类型不正确", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_07(self):
        """推送正式设备数据-字段类型不正确double->string"""
        data = soil_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data['temp'] = "string"
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("temp字段类型不正确", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_08(self):
        """推送正式设备数据-字段类型不正确 datetime->string"""
        data = soil_data.JSONV2_Request(self.NdeviceId)
        data['deviceTime'] = "deviceTime-string"
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("deviceTime字段类型不正确", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_09(self):
        """推送正式设备数据-设备ID不存在"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = soil_data.JSONV2_Request("soil-NotExist")
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("未找到设备", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_10(self):
        """推送正式设备数据-设备未激活"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = soil_data.JSONV2_Request("soil-NotActive")
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("设备未激活", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_22(self):
        """推送正式设备数据-json 格式不正确"""
        data = soil_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        data = data[:-1]
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("json格式不正确", elkLog['exceptionContent'], elkLog)
        self.assertEqual(2, elkLog['uploadStatus'])


if __name__ == '__main__':

    unittest.main(verbosity=2)
