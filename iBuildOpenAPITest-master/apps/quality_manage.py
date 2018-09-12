#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import requests.packages.urllib3.util.ssl_
from random import randint
import os
import uuid
import urllib3
from faker import Faker
dir_path = os.path.dirname(os.path.abspath(__file__ + "/../"))
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
urllib3.disable_warnings()


def JSONV2_Request(ProjectSysNo):
    dataTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fake = Faker("zh_CN")
    tmpreq = {
        "projectSysNo": str(ProjectSysNo),
        "sourceId": str(uuid.uuid4()),
        "checkDate": dataTime,
        "checkUserId": "5/21/33",
        "checkUserName": "张三/李四/王五",
        "checkDetail": fake.text(),
        "checkUnitId": str(uuid.uuid4()),
        "checkUnitName": fake.company(),
        "problemLevel": randint(0, 2),
        "rectifyRequire": fake.text(),
        "itemClassifactionsId": str(uuid.uuid4()),
        "itemClassifactionsName": fake.text(max(range(5, 10))),
        "partitioningId": "221/541/632/898",
        "partitioningName": "xx楼/xx层/xx段/xx部位名称",
        "rectifyUnitId": str(uuid.uuid4()),
        "rectifyUnitName": fake.company(),
        "rectifyUserId": str(uuid.uuid4()),
        "rectifyUserName": fake.name(),
        "rectifyUserDate": dataTime,
        "rectifyDescription": fake.text(max(range(5, 10))),
        "reviewUserId": "279281",
        "reviewUserName": fake.name(),
        "reviewDescription": fake.text(max(range(5, 10))),
        "reviewDate": dataTime,
        "reviewUnitId": str(uuid.uuid4()),
        "reviewUnitName": fake.company(),
        "rectifyStatus": 0,
        "checkStatus": 3,
        "attachmentList": [{
            "fileName": "xxx.png",
            "fileType": 0,
            "fileUrl": "http://image.xxx.com/xxx.png",
            "businessType": 1
        }],
        "deleted": False
    }

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request(10218), indent=4, ensure_ascii=False))
