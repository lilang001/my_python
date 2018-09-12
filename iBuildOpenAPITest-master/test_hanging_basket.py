#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from OpenAPI import OpenAPI
from config import elkSearch, pyMongodb, Check
import os, time
import HtmlTestRunner
from apps import hanging_basket as hanging_basket_data
dir_path = os.path.dirname(os.path.realpath(__file__))


class hanging(unittest.TestCase):
    def setUp(self):
        self.mongo = pyMongodb.pymongo()
        self.method = 'upload.hangingBasketLiveData'
        self.NdeviceId = 'hanging'

    def test_01(self):
        """推送测试设备数据"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual(None, elkLog['exceptionContent'])

        mongoLog = self.mongo.getbyDeviceTime(deviceTime, "hanging_basket")

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
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        del data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        # elkLog = elkSearch.elkDevice(deviceTime, self.method)

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

    def test_03(self):
        """推送测试设备数据-无currentCounterWeight字段"""
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data["currentCounterWeight"]
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("currentCounterWeight字段不能为空",
                         elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_04(self):
        """推送测试设备数据-无currentLoadWeight字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['currentLoadWeight']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("currentLoadWeight字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_05(self):
        """推送测试设备数据-无waver字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['waver']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("waver字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_06(self):
        """推送测试设备数据-无swingAngle字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['swingAngle']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("swingAngle字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_07(self):
        """推送测试设备数据-无currentHeight字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['currentHeight']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("currentHeight字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    """
    def test_08(self):
        "推送测试设备数据-无buckleCount字段"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['buckleCount']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("buckleCount字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])
    """

    def test_09(self):
        """推送测试设备数据-无personCount字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['personCount']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("personCount字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    """
    def test_10(self):
        "推送测试设备数据-无groupList字段"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['groupList']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("groupList字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])
    """

    def test_11(self):
        """推送测试设备数据-无wireState字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['groupList'][0]['wireState']  # 清空list
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("wireState字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_012(self):
        """推送测试设备数据-推送未定义字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data['pm110'] = 100
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_013(self):
        """推送正式设备数据-字段类型不正确double->string"""
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data['currentCounterWeight'] = "string"
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("currentCounterWeight字段类型不正确",
                         elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_014(self):
        """推送正式设备数据-字段类型不正确 datetime->string"""
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        data['deviceTime'] = "deviceTime-string"
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("deviceTime字段类型不正确", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_015(self):
        """推送正式设备数据-字段类型不正确 int->double"""
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        data['personCount'] = 100.921
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("personCount字段类型不正确", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_016(self):
        """推送正式设备数据-字段类型不正确 list->double"""
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
        data['groupList'] = 100 / 10.0
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("groupList字段类型不正确", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_017(self):
        """推送正式设备数据-设备ID不存在"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hanging_basket_data.JSONV2_Request("hanging-NotExist")
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("未找到设备", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_018(self):
        """推送正式设备数据-设备未激活"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = hanging_basket_data.JSONV2_Request("hanging-NotActive")
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("设备未激活", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_22(self):
        """推送正式设备数据-json 格式不正确"""
        data = hanging_basket_data.JSONV2_Request(self.NdeviceId)
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
    # t = hanging()
    # t.setUp()
    # t.test_015()
