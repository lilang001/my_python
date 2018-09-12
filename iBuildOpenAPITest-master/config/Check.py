#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import pyMongodb
# import pyMongodb
import json
from datetime import datetime

elkres = {
    'dataContent':
    '{"deviceId": "hanging", "longitude": 71.8, "latitude": 61.1, "stdLoadWeight": 229.0, "stdCounterWeight": 2, "errorCounterWeight": 0, "maxWaver": 0.3, "maxSwingAngle": 0.0, "maxPersonCount": 7, "minTopHeight": 5}',
    '@timestamp': '2018-08-01T10|43| 34.097Z',
    'method': 'upload.hangingBasketDeviceParams',
    '@version': '1',
    'operationType': 'deviceParams',
    'id': '6a6772b6653f4366a322c69a191a74eb',
    'type': 'ibuild-data-log',
    'supplierSysNo': 200114,
    'uploadTime': '2018-08-01T10:43:33Z',
    'version': '1.0',
    'appName': '智能吊篮',
    'environmentType': 1,
    'dataType': 1,
    'catalogCode': 'hanging_basket',
    'uploadStatus': 1,
    'deviceCode': 'hanging',
    'appCode': 'hanging_basket',
    'deviceTime': None,
    'productSysNo': 20409,
    'projectSysNo': 10266,
    'dataSysNo': 'd1be97a863244b93910790dba0efbcd4',
    'exceptionContent': None,
    'deviceSysNo': 11645,
    'projectName': '数据推送测试项目-勿动'
}

reqdata = {
    "deviceId": "hanging",
    "longitude": 71.8,
    "latitude": 61.1,
    "stdLoadWeight": 229.0,
    "stdCounterWeight": 2,
    "errorCounterWeight": 0,
    "maxWaver": 0.3,
    "maxSwingAngle": 0.0,
    "maxPersonCount": 7,
    "minTopHeight": 5
}

# pym = pyMongodb.pymongo()
# mongores = pym.getbyDeviceTime("2018-07-27 14:4:46", "env_monitor")


def dataCheck(mongores="", elkres="", reqdata=""):
    Mongo_ELK_Match = True
    Mongo_ReqData_Match = True
    ELK_ReqData_Match = True
    elkres = json.loads(elkres['dataContent'])
    if len(mongores) > 0:
        if 'groupList' in mongores:
            del mongores['groupList']
        for k, v in mongores.items():
            if isinstance(v, datetime):
                elkres[k] = datetime.utcfromtimestamp(
                    datetime.strptime(elkres[k], "%Y-%m-%d %H:%M:%S")
                    .timestamp())
                if str(elkres[k]) != str(mongores[k]):
                    print(k + "E_M Not Match!")
                    print(elkres[k], mongores[k])
                    print(type(elkres[k]), type(mongores[k]))
                    Mongo_ELK_Match = False
            if str(elkres[k]) != str(mongores[k]):
                print(k + "E_M Not Match!")
                print(elkres[k], mongores[k])
                print(type(elkres[k]), type(mongores[k]))
                Mongo_ELK_Match = False
        for k, v in mongores.items():
            if isinstance(v, datetime):
                reqdata[k] = datetime.utcfromtimestamp(
                    datetime.strptime(reqdata[k], "%Y-%m-%d %H:%M:%S")
                    .timestamp())
                if str(reqdata[k]) != str(mongores[k]):
                    print(k + "R_M Not Match!")
                    print(elkres[k], mongores[k])
                    print(type(elkres[k]), type(mongores[k]))
                    Mongo_ReqData_Match = False
            if str(reqdata[k]) != str(mongores[k]):
                print(k + "R_M Not Match!")
                print(elkres[k], mongores[k])
                print(type(elkres[k]), type(mongores[k]))
                Mongo_ReqData_Match = False

    for k, v in elkres.items():
        if isinstance(v, datetime):
            if reqdata[k] != elkres[k]:
                # print(k + "R_E Not Match!")
                # print(elkres[k], elkres[k])
                # print(type(elkres[k]), type(elkres[k]))
                ELK_ReqData_Match = False
        if reqdata[k] != elkres[k]:
            ELK_ReqData_Match = False
    return Mongo_ELK_Match, Mongo_ReqData_Match, ELK_ReqData_Match


if __name__ == "__main__":
    a, b, c = dataCheck(mongores=mongores, elkres=elkres, reqdata=reqdata)
    print(a, b, c)
