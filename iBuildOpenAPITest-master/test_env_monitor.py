#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from OpenAPI import OpenAPI
from config import elkSearch, pyMongodb, Check
import os, time
import HtmlTestRunner
from apps import env_monitor as env_data
dir_path = os.path.dirname(os.path.realpath(__file__))


class env_monitor(unittest.TestCase):
    def setUp(self):
        self.mongo = pyMongodb.pymongo()
        self.method = 'upload.envMonitorLiveData'
        self.NdeviceId = 'OpenAPI'

    def test_01(self):
        """推送正式设备数据"""
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual(1, elkLog['uploadStatus'], elkLog)

        mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")
        del mongoLog['aqiValue']

        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")

    def test_02(self):
        """推送正式设备数据-无deviceTime字段"""
        data = env_data.JSONV2_Request(self.NdeviceId)
        del data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

    def test_03(self):
        """推送正式设备数据-无pm25字段"""
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['pm25']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("pm25字段不能为空", elkLog['exceptionContent'], elkLog)

        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_04(self):
        """推送正式设备数据-无pm10字段"""
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['pm10']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("pm10字段不能为空", elkLog['exceptionContent'], elkLog)

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_05(self):
        """推送正式设备数据-推送未定义字段"""
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data['pm110'] = 100
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual(1, elkLog['uploadStatus'])
        mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")
        del mongoLog['aqiValue']
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_06(self):
        """推送正式设备数据-字段类型不正确int->string"""
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data['pm10'] = "string"
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("pm10字段类型不正确", elkLog['exceptionContent'], elkLog)
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_07(self):
        """推送正式设备数据-字段类型不正确 datetime->string"""
        data = env_data.JSONV2_Request(self.NdeviceId)
        data['deviceTime'] = "deviceTime-string"
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("deviceTime字段类型不正确", elkLog['exceptionContent'],
                         elkLog)
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_08(self):
        """推送正式设备数据-设备ID不存在"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = env_data.JSONV2_Request("OpenAPI-NotExist")
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("未找到设备", elkLog['exceptionContent'], elkLog)
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_09(self):
        "推送正式设备数据-设备未激活"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = env_data.JSONV2_Request("OpenAPI-NotActive")
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("设备未激活", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    """
    def test_10(self):
        "推送正式设备数据-项目已删除设备"
        data = env_data.JSONV2_Request("OpenAPI-DelDevice")
        deviceTime = data['deviceTime']
        deviceId = data['deviceId']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("在激活项目中未找到该设备",
        elkLog['exceptionContent'],elkLog)
        self.assertEqual(deviceId, elkLog['deviceCode'])

    def test_11(self):
        "推送正式设备数据-项目删除应用"
        data = env_data.JSONV2_Request("Open-API-DelApp")
        deviceTime = data['deviceTime']
        deviceId = data['deviceId']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("在激活项目中未找到智慧应用",
        elkLog['exceptionContent'],elkLog)
        self.assertEqual(deviceId, elkLog['deviceCode'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_12(self):
        "推送正式设备数据-数据超长"
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        data['pm25'] = 10000000000000000
        deviceId = data['deviceId']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("pm25 字段超长", elkLog['exceptionContent'],elkLog)
        self.assertEqual(deviceId, elkLog['deviceCode'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_13(self):
        "推送正式设备数据-风向超过360度"
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        deviceId = data['deviceId']
        data['windDirect'] = 400.0001
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("windDirect超过360", elkLog['exceptionContent'],elkLog)
        self.assertEqual(deviceId, elkLog['deviceCode'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_14(self):
        "推送正式设备数据-pm25 小数位数超过1位"
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        deviceId = data['deviceId']
        data['pm25'] = 40.0001
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("pm25 小数位数超过1位",
        elkLog['exceptionContent'],elkLog)
        self.assertEqual(deviceId, elkLog['deviceCode'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_15(self):
        "推送正式设备数据-pm10 小数位数超过1位"
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        deviceId = data['deviceId']
        data['pm10'] = 40.0001
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("pm10 小数位数超过1位",
        elkLog['exceptionContent'],elkLog)
        self.assertEqual(deviceId, elkLog['deviceCode'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_16(self):
        "推送正式设备数据-tsp 小数位数超过1位"
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        deviceId = data['deviceId']
        data['tsp'] = 40.0001
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("tsp 小数位数超过1位",
        elkLog['exceptionContent'],elkLog)
        self.assertEqual(deviceId, elkLog['deviceCode'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_17(self):
        "推送正式设备数据-noise 小数位数超过1位"
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        deviceId = data['deviceId']
        data['noise'] = 40.0001
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("noise 小数位数超过1位",
        elkLog['exceptionContent'],elkLog)
        self.assertEqual(deviceId, elkLog['deviceCode'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_18(self):
        "推送正式设备数据-windSpeed 小数位数超过1位"
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        deviceId = data['deviceId']
        data['windSpeed'] = 40.0001
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("windSpeed 小数位数超过1位",
        elkLog['exceptionContent'],elkLog)
        self.assertEqual(deviceId, elkLog['deviceCode'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_19(self):
        "推送正式设备数据-temp 小数位数超过1位"
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        deviceId = data['deviceId']
        data['temp'] = 40.0001
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("temp 小数位数超过1位",
        elkLog['exceptionContent'],elkLog)
        self.assertEqual(deviceId, elkLog['deviceCode'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_20(self):
        "推送正式设备数据-humid 小数位数超过1位"
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        deviceId = data['deviceId']
        data['humid'] = 40.0001
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("humid 小数位数超过1位",
        elkLog['exceptionContent'],elkLog)
        self.assertEqual(deviceId, elkLog['deviceCode'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_21(self):
        "推送正式设备数据-atoms 小数位数超过1位"
        data = env_data.JSONV2_Request(self.NdeviceId)
        deviceTime = data['deviceTime']
        deviceId = data['deviceId']
        data['atoms'] = 40.0001
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("atoms 小数位数超过1位",
        elkLog['exceptionContent'],elkLog)
        self.assertEqual(deviceId, elkLog['deviceCode'])
        self.assertEqual(2, elkLog['uploadStatus'])

    """

    def test_22(self):
        """推送正式设备数据-json 格式不正确"""
        data = env_data.JSONV2_Request(self.NdeviceId)
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
    # env = env_monitor()
    # env.setUp()
    # env.test_06()
    # env.test_07()
    # env.test_22()
