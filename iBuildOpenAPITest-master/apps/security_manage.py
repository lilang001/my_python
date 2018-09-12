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
        "checkUserId": str(uuid.uuid4()),
        "checkUserName": fake.name(),
        "checkDetail": fake.text(max(range(10, 15))),
        "checkUnitId": "checkUnitId-" + str(randint(1, 10)),
        "checkUnitName": fake.company(),
        "problemLevel": randint(0, 2),
        "rectifyRequire": fake.text(),
        "subItemId": "142/331/422",
        "subItemName": "地基与基础/基础/钢筋混凝土扩展基础",
        "partitioningId": "221/541/632/898",
        "partitioningName": "xx楼/xx层/xx段/xx部位名称",
        "rectifyUnitId": str(uuid.uuid4()),
        "rectifyUnitName": fake.company(),
        "rectifyUserId": str(uuid.uuid4()),
        "rectifyUserName": fake.name(),
        "rectifyUserDate": dataTime,
        "rectifyDescription": fake.text(),
        "reviewUserId": "279281",
        "reviewUserName": fake.name(),
        "reviewDescription": "复查描述:" + fake.text(),
        "reviewUnitId": str(uuid.uuid4()),
        "reviewUnitName": fake.company(),
        "reviewDate": dataTime,
        "rectifyStatus": randint(0, 4),
        "checkStatus": randint(0, 1),
        "deleted": False,
        "attachmentList": [{
            "fileName": "xxx.png",
            "fileType": randint(0, 1),
            "fileUrl": "http://image.xxx.com/xxx.png",
            "businessType": randint(0, 3)
        }]
    }

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request(10218), indent=4, ensure_ascii=False))
