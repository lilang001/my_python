#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
from OpenAPI import OpenAPI
from config import elkSearch, pyMongodb, Check
import os, time
import HtmlTestRunner
from apps import process_manage as process_task
from faker import Faker
from datetime import datetime
import tzlocal
import pytz
from config import AppConfig
dir_path = os.path.dirname(os.path.realpath(__file__))

local_timezone = tzlocal.get_localzone()  # get pytz tzinfo


class process(unittest.TestCase):
    def setUp(self):
        self.mongo = pyMongodb.pymongo()
        self.method = 'upload.processTaskData'
        self.ProjectSysNo = AppConfig.ENV['SoftwareProjectSysNo']

    def test_01(self):
        "推送正式项目数据"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']

        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(1, elkLog['uploadStatus'])
        self.assertEqual(self.ProjectSysNo, elkLog['projectSysNo'])

        mongoLog = self.mongo.getbySourceId(sourceId, "process_task")
        if "partitioningList" in mongoLog:
            del mongoLog['partitioningList']
        if "submitUserList" in mongoLog:
            del mongoLog['submitUserList']
        if "responsibleUserList" in mongoLog:
            del mongoLog['responsibleUserList']

        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")
        self.assertEqual(0, res.json()['code'])

    def test_02(self):
        "推送测试项目数据"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(self.ProjectSysNo, elkLog['projectSysNo'])
        self.assertEqual(0, res.json()['code'])

    def test_03(self):
        "推送正式项目数据- 无projectSysNo"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['projectSysNo']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual(2, elkLog['uploadStatus'], elkLog)
        self.assertEqual("projectSysNo字段不能为空", elkLog['exceptionContent'],
                         sourceId)

    def test_04(self):
        "推送正式项目数据- 无sourceId"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['sourceId']
        data['parentSourceId'] = sourceId
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual(2, elkLog['uploadStatus'], elkLog)
        self.assertEqual("sourceId字段不能为空", elkLog['exceptionContent'],
                         sourceId)

    def test_05(self):
        "推送正式项目数据- 无name"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['name']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual(2, elkLog['uploadStatus'], elkLog)
        self.assertEqual("name字段不能为空", elkLog['exceptionContent'], sourceId)

    def test_06(self):
        "推送正式项目数据- 无sortIndex"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['sortIndex']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual(2, elkLog['uploadStatus'], elkLog)
        self.assertEqual("sortIndex字段不能为空", elkLog['exceptionContent'],
                         sourceId)

    def test_07(self):
        "推送正式项目数据- 无planStartTime"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['planStartTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual(2, elkLog['uploadStatus'], elkLog)
        self.assertEqual("planStartTime字段不能为空", elkLog['exceptionContent'],
                         sourceId)

    def test_08(self):
        "推送正式项目数据- 无planEndTime"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['planEndTime']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual(2, elkLog['uploadStatus'], elkLog)
        self.assertEqual("planEndTime字段不能为空", elkLog['exceptionContent'],
                         sourceId)

    def test_09(self):
        "推送正式项目数据- 无status"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        del data['status']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual(2, elkLog['uploadStatus'], elkLog)
        self.assertEqual("status字段不能为空", elkLog['exceptionContent'], sourceId)

    def test_10(self):
        "推送正式项目数据- 字段类型不一致 datetime->string"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data['actualStartTime'] = 'actualStartTime'
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual(2, elkLog['uploadStatus'], elkLog)
        self.assertEqual("actualStartTime字段类型不正确", elkLog['exceptionContent'],
                         elkLog)

    def test_11(self):
        "推送正式项目数据- 有未定义的节点"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data['undefind_node'] = 'undefind_node'
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])

        mongoLog = self.mongo.getbySourceId(sourceId, "process_task")
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")
        if "partitioningList" in mongoLog:
            del mongoLog['partitioningList']
        if "submitUserList" in mongoLog:
            del mongoLog['submitUserList']
        if "responsibleUserList" in mongoLog:
            del mongoLog['responsibleUserList']

        Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match = Check.dataCheck(
            mongores=mongoLog, elkres=elkLog, reqdata=json.loads(data))
        self.assertTrue(Mongo_ELK_Match, "Mongo_ELK check Fail")
        self.assertTrue(Mongo_ReqData_Match, "Mongo_ReqData check Fail")
        self.assertTrue(ELK_ReqData_Match, "ELK_ReqData check Fail")

    def test_12(self):
        "推送正式项目数据- 项目未添加应用"
        data = process_task.JSONV2_Request(10)
        sourceId = data['sourceId']
        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("不能使用该项目", elkLog['exceptionContent'])

    """
    def test_13(self):
        "推送正式项目数据- 数据超长"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        fake = Faker("zh_CN")
        data['partitioningName'] = fake.text(max(range(2500, 3000)))

        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("partitioningName字段超长", elkLog['exceptionContent'])

    def test_14(self):
        "推送正式项目数据- type 超出枚举"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data['type'] = 9

        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("type 超出枚举范围", elkLog['exceptionContent'])

    def test_15(self):
        "推送正式项目数据- status 超出枚举"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data['status'] = 9

        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("status 超出枚举范围", elkLog['exceptionContent'])

    def test_16(self):
        "推送正式项目数据- completionRate 小于0"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data['completionRate'] = -9

        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("completionRate 小于0", elkLog['exceptionContent'])

    def test_17(self):
        "推送正式项目数据- completionRate 大于100"
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data['completionRate'] = 190

        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(0, res.json()['code'])
        self.assertEqual("completionRate 大于100", elkLog['exceptionContent'])
    """

    def test_18(self):
        "推送正式项目数据- 根据sourceId更新软件数据"
        pdata = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = pdata['sourceId']
        pdata = json.dumps(pdata)
        pres = OpenAPI(method=self.method, data=pdata)
        self.assertEqual(0, pres.json()['code'], "Send OpenAPI Fail")

        fake = Faker('zh_CN')
        data = json.loads(pdata)
        # 转换UTC时间为本地时间
        for k, v in data.items():
            if isinstance(k, datetime):
                data[k] = data[k].replace(
                    tzinfo=pytz.utc).astimezone(local_timezone)
        data['completionRate'] = data['completionRate'] + 1
        data['actualEndTime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['partitioningName'] = fake.text(max(range(10, 500)))

        data = json.dumps(data)
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'], "Send OpenAPI Fail")

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual(1, elkLog['uploadStatus'], elkLog)

    def test_22(self):
        """推送正式设备数据-json 格式不正确"""
        data = process_task.JSONV2_Request(self.ProjectSysNo)
        sourceId = data['sourceId']
        data = json.dumps(data)
        data = data[:-1]
        res = OpenAPI(method=self.method, data=data)
        self.assertEqual(0, res.json()['code'])

        elkLog = elkSearch.elkSoftware(sourceId, self.method)
        self.assertEqual("json格式不正确", elkLog['exceptionContent'], elkLog)
        self.assertEqual(2, elkLog['uploadStatus'])


if __name__ == '__main__':
    # unittest.main(verbosity=2)
    env = process()
    env.setUp()
    env.test_12()
