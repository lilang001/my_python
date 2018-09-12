#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from OpenAPI import OpenAPI
from config import elkSearch, pyMongodb, Check
import os, time
import HtmlTestRunner
from apps import security_manage as securityCheck
from faker import Faker
from datetime import datetime
import tzlocal
import pytz
from config import AppConfig
dir_path = os.path.dirname(os.path.realpath(__file__))

local_timezone = tzlocal.get_localzone()  # get pytz tzinfo


class security(unittest.TestCase):
    def setUp(self):
        self.mongo = pyMongodb.pymongo()
        self.method = 'upload.securityCheckData'
        self.ProjectSysNo = AppConfig.ENV['SoftwareProjectSysNo']

    def test_01(self):
        "推送正式项目数据"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']

        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(self.ProjectSysNo, elkLog['projectSysNo'])

        mongoLog = self.mongo.getbySourceId(sourceId, "security_check")
        if 'checkUserList' in mongoLog:
            del mongoLog['checkUserList']
        if 'partitioningList' in mongoLog:
            del mongoLog['partitioningList']

        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_02(self):
        "推送测试项目数据"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(self.ProjectSysNo, elkLog['projectSysNo'])
        self.assertEqual(0, res.json()['code'])

    def test_03(self):
        "推送正式项目数据- 无projectSysNo"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['projectSysNo']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("projectSysNo字段不能为空", elkLog['exceptionContent'])

    def test_04(self):
        "推送正式项目数据- 无sourceId"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['sourceId']
        data['parentSourceId'] = sourceId
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("sourceId字段不能为空", elkLog['exceptionContent'])

    def test_05(self):
        "推送正式项目数据- 无checkDate"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['checkDate']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("checkDate字段不能为空", elkLog['exceptionContent'])

    def test_06(self):
        "推送正式项目数据- 无checkUserId"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['checkUserId']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("checkUserId字段不能为空", elkLog['exceptionContent'])

    def test_07(self):
        "推送正式项目数据- 无checkUserName"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['checkUserName']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("checkUserName字段不能为空", elkLog['exceptionContent'])

    def test_08(self):
        "推送正式项目数据- 无checkStatus"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['checkStatus']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("checkStatus字段不能为空", elkLog['exceptionContent'])

    def test_09(self):
        "推送正式项目数据- 无rectifyStatus"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['rectifyStatus']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("rectifyStatus字段不能为空", elkLog['exceptionContent'])

    def test_10(self):
        "推送正式项目数据- 字段类型不一致 datetime->string"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data['checkDate'] = 'actualStartTime'
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("checkDate字段类型不正确", elkLog['exceptionContent'])

    def test_11(self):
        "推送正式项目数据- 有未定义的节点"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data['undefind_node'] = 'undefind_node'
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        mongoLog = self.mongo.getbySourceId(sourceId, "security_check")
        if 'checkUserList' in mongoLog:
            del mongoLog['checkUserList']
        if 'partitioningList' in mongoLog:
            del mongoLog['partitioningList']
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")

    """
    def test_12(self):
        "推送正式项目数据- 数据超长"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        fake = Faker("zh_CN")
        data['partitioningName'] = fake.text(max(range(2500, 3000)))

        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("partitioningName字段超长", elkLog['exceptionContent'])

    def test_13(self):
        "推送正式项目数据- rectifyStatus 超出枚举"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data['rectifyStatus'] = 9

        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("rectifyStatus 超出枚举范围", elkLog['exceptionContent'])

    def test_14(self):
        "推送正式项目数据- problemLevel 超出枚举"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data['problemLevel'] = 9

        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("problemLevel 超出枚举范围", elkLog['exceptionContent'])

    def test_15(self):
        "推送正式项目数据- checkStatus 超出枚举"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data['checkStatus'] = 9

        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("checkStatus 超出枚举范围", elkLog['exceptionContent'])
    """

    def test_16(self):
        "推送正式项目数据- 根据sourceId更新软件数据"
        pdata = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = pdata['sourceId']
        pdata = json.dumps(pdata)
        pres = OpenAPI(method=self.method, data=pdata)
        self.assertEqual(0, pres.json()['code'], "Send OpenAPI Fail")

        data = json.loads(pdata)
        fake = Faker("zh_CN")
        # data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        # 转换UTC时间为本地时间
        for k, v in data.items():
            if isinstance(k, datetime):
                data[k] = data[k].replace(
                    tzinfo=pytz.utc).astimezone(local_timezone)
        data['rectifyDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['reviewUserName'] = fake.name()

        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(1, elkLog['uploadStatus'])

    def test_17(self):
        "推送正式项目数据- 无partitioningId"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['partitioningId']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("partitioningId字段不能为空", elkLog['exceptionContent'])

    def test_18(self):
        "推送正式项目数据- 无partitioningName"
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['partitioningName']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("partitioningName字段不能为空", elkLog['exceptionContent'])

    def test_21(self):
        "推送正式项目数据- 项目未添加应用"
        data = securityCheck.JSONV2_Request(10)
        sourceId = data['sourceId']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("不能使用该项目", elkLog['exceptionContent'])

    def test_22(self):
        """推送正式设备数据-json 格式不正确"""
        data = securityCheck.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data = json.dumps(data)
        data = data[:-1]
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual("json格式不正确", elkLog['exceptionContent'], elkLog)
        self.assertEqual(2, elkLog['uploadStatus'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
    # env = security()
    # env.setUp()
    # env.test_01()
    # env.test_01()
