#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from OpenAPI import OpenAPI
from config import elkSearch, pyMongodb, Check
import os, time
from datetime import datetime
from apps import vehicle_management as vehicle
dir_path = os.path.dirname(os.path.realpath(__file__))


class vehicle_management(unittest.TestCase):
    def setUp(self):
        self.mongo = pyMongodb.pymongo()
        self.method = 'upload.vehicleManagementLiveData'
        self.NdeviceId = 'vehicle'

    def test_01(self):
        "推送正式设备数据"
        data = vehicle.JSONV2_Request(deviceID=self.NdeviceId)
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual(1, elkLog['uploadStatus'], elkLog)

        mongoLog = self.mongo.getbyDeviceTime(deviceTime, "vehicle_management")

        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")

    def test_02(self):
        "推送正式设备数据-无deviceTime字段"
        data = vehicle.JSONV2_Request(deviceID=self.NdeviceId)
        del data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

    def test_03(self):
        "推送正式设备数据-无vehicleNumber字段"
        data = vehicle.JSONV2_Request(deviceID=self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['vehicleNumber']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("vehicleNumber字段不能为空", elkLog['exceptionContent'])

    def test_04(self):
        "推送正式设备数据-推送未定义字段"
        data = vehicle.JSONV2_Request(deviceID=self.NdeviceId)
        deviceTime = data['deviceTime']
        data['pm110'] = 100
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual(1, elkLog['uploadStatus'])
        mongoLog = self.mongo.getbyDeviceTime(deviceTime, "vehicle_management")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_06(self):
        "推送正式设备数据-字段类型不正确 datetime->string"
        data = vehicle.JSONV2_Request(deviceID=self.NdeviceId)
        data['deviceTime'] = "deviceTime-string"
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("deviceTime字段类型不正确", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_07(self):
        "推送正式设备数据-设备ID不存在"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = vehicle.JSONV2_Request(deviceID="vehicle-NotExist")
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("未找到设备", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    def test_08(self):
        "推送正式设备数据-设备未激活"
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = vehicle.JSONV2_Request(deviceID="vehicle-NotActive")
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("设备未激活", elkLog['exceptionContent'])
        self.assertEqual(2, elkLog['uploadStatus'])

    """
    def test_11(self):
        "推送正式设备数据-数据超长"
        data = vehicle.JSONV2_Request(deviceID=self.NdeviceId)
        deviceTime = data['deviceTime']
        data['usingCount'] = 10000000000000000
        deviceId = data['deviceId']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("usingCount 字段超长", elkLog['exceptionContent'])
        self.assertEqual(deviceId, elkLog['deviceCode'])
        self.assertEqual(2, elkLog['uploadStatus'])
    """

    def test_12(self):
        "推送正式设备数据-无entryOrExit字段"
        data = vehicle.JSONV2_Request(deviceID=self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['entryOrExit']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("entryOrExit字段不能为空", elkLog['exceptionContent'])

    """
    def test_13(self):
        "推送正式设备数据-entryOrExit超出枚举"
        data = vehicle.JSONV2_Request(deviceID=self.NdeviceId)
        deviceTime = data['deviceTime']
        data['entryOrExit'] = 9
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("entryOrExit超出枚举", elkLog['exceptionContent'])
    """

    def test_14(self):
        "推送正式设备数据-无entryOrExitTime字段"
        data = vehicle.JSONV2_Request(deviceID=self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['entryOrExitTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("entryOrExitTime字段不能为空", elkLog['exceptionContent'])

    def test_15(self):
        "推送正式设备数据-无registeredVehicle字段"
        data = vehicle.JSONV2_Request(deviceID=self.NdeviceId)
        deviceTime = data['deviceTime']
        del data['registeredVehicle']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("registeredVehicle字段不能为空", elkLog['exceptionContent'])

    """
    def test_17(self):
        "推送正式设备数据-regiteredVehicle超出枚举"
        data = vehicle.JSONV2_Request(deviceID=self.NdeviceId)
        deviceTime = data['deviceTime']
        data['regiteredVehicle'] = 3
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("regiteredVehicle超出枚举", elkLog['exceptionContent'])
    """

    def test_22(self):
        """推送正式设备数据-json 格式不正确"""
        data = vehicle.JSONV2_Request(deviceID=self.NdeviceId)
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
    # env = vehicle_management()
    # env.setUp()
    # env.test_04()
