#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json
import os
from OpenAPI import OpenAPI
from datetime import datetime
import HtmlTestRunner
dir_path = os.path.dirname(os.path.realpath(__file__))


class OpenAPISign(unittest.TestCase):
    def setUp(self):
        self.method = 'upload.envMonitorLiveData'

    def test_SignCase_1(self):
        """ appid 不正确"""
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
        res = OpenAPI(p_appid='ss', method=self.method, data=data)

        self.assertEqual("无API访问权限",
                         res.json()['message'], "Send OpenAPI Fail")

    def test_SignCase_2(self):
        """ appsecret 不正确"""
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
        res = OpenAPI(p_appsecret='ss', method=self.method, data=data)

        self.assertEqual("签名校验错误", res.json()['message'], "Send OpenAPI Fail")

    def test_SignCase_3(self):
        """ format<>json 不正确"""
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
        res = OpenAPI(p_format='ss', method=self.method, data=data)

        self.assertEqual("请求参数format错误",
                         res.json()['message'], "Send OpenAPI Fail")

    def test_SignCase_4(self):
        """ version 不正确"""
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
        res = OpenAPI(p_version='ss', method=self.method, data=data)

        self.assertEqual("请求参数version错误",
                         res.json()['message'], "Send OpenAPI Fail")

    def test_SignCase_5(self):
        """ timestamp 超过10分钟"""
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
        res = OpenAPI(p_time='20170215101958', method=self.method, data=data)

        self.assertEqual("时间戳已超过10分钟的范围",
                         res.json()['message'], "Send OpenAPI Fail")


if __name__ == '__main__':
    unittest.main(verbosity=2)
    # run = OpenAPISign()
    # res = run.test_SignCase_3()
