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


class env_monitor_testDevice(unittest.TestCase):
    def setUp(self):
        self.mongo = pyMongodb.pymongo()
        self.method = 'upload.envMonitorLiveData'

    def test_env_01(self):
        """推送测试设备数据"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = env_data.JSONV2_Request("OpenAPI-Test")
        deviceTime = data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")
        # if 'aqiValue' in mongoLog:
        # del mongoLog['aqiValue']

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_env_02(self):
        """推送测试设备数据-无deviceTime字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = env_data.JSONV2_Request("OpenAPI-Test")
        del data['deviceTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        # elkLog = elkSearch.elkDevice(deviceTime, self.method)

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

    def test_env_03(self):
        """推送测试设备数据-无pm25字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = env_data.JSONV2_Request("OpenAPI-Test")
        deviceTime = data['deviceTime']
        del data['pm25']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("pm25字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

    def test_env_04(self):
        """推送测试设备数据-无pm10字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = env_data.JSONV2_Request("OpenAPI-Test")
        deviceTime = data['deviceTime']
        del data['pm10']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)
        self.assertEqual("pm10字段不能为空", elkLog['exceptionContent'])

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_env_05(self):
        """推送测试设备数据-推送未定义字段"""
        # mongo = pyMongodb.pymongo('172.16.0.137', 20200)
        data = env_data.JSONV2_Request("OpenAPI-Test")
        deviceTime = data['deviceTime']
        data['pm110'] = 100
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkDevice(deviceTime, self.method)

        # mongoLog = self.mongo.getbyDeviceTime(deviceTime, "env_monitor")
        # if 'aqiValue' in mongoLog:
        # del mongoLog['aqiValue']

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])


if __name__ == '__main__':

    unittest.main(verbosity=2)
