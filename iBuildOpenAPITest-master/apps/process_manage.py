#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import requests.packages.urllib3.util.ssl_
from random import randint
import os
import uuid
import urllib3
from random import choice
from faker import Faker
dir_path = os.path.dirname(os.path.abspath(__file__ + "/../"))
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
urllib3.disable_warnings()


def JSONV2_Request(ProjectSysNo):
    dataTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fake = Faker("zh_CN")
    tmpreq = {
        "projectSysNo": str(ProjectSysNo),
        "processPlanId": str(uuid.uuid4()),
        "processPlanName": fake.text(max(range(5, 15))),
        "sourceId": str(uuid.uuid4()),
        "parentSourceId": str(uuid.uuid4()),
        "name": "AutoTestName" + dataTime,
        "level": randint(0, 10),
        "sortIndex": randint(0, 10),
        "leaf": choice([True, False]),
        "responsibleUserId": "5/65/242",
        "responsibleUserName": "张三/李四/王五",
        "submitUserId": "5/65/242",
        "submitUserName": "张三/李四/王五",
        "planStartTime": dataTime,
        "planEndTime": dataTime,
        "actualStartTime": dataTime,
        "actualEndTime": dataTime,
        "type": 1,
        "partitioningId": str(uuid.uuid4()),
        "partitioningName": "AutoTest-partitioningName" + dataTime,
        "completionRate": randint(0, 20) / 1.0,
        "status": 1,
        "deleted": False
    }

    return tmpreq


if __name__ == "__main__":
    # print(XML_Request("data_collect","sg001"))
    print(json.dumps(JSONV2_Request(10218), indent=4, ensure_ascii=False))
