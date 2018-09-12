#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from datetime import datetime
from .AppConfig import ENV


class pymongo():
    def __init__(self):
        if ENV['Env'] == 'QA':
            self.client = MongoClient(
                '172.16.0.137', 20200, username='admin', password='yzw@123')
        if ENV['Env'] == 'PRD':
            self.client = MongoClient(
                '192.168.110.86',
                20200,
                username='ibuildData',
                password='YzwIbuild2018',
                authSource='ibuild_data')

    def aggregate(self, pip, collection):
        db = self.client.ibuild_data
        result = db[collection].aggregate(pip)
        res = []
        for r in result:
            # print(r)
            res.append(r)
        return res[0]

    def getbySourceId(self, sourceID, collection):
        db = self.client.ibuild_data
        pip = [{
            "$match": {
                "sourceId": {
                    "$in": [sourceID]
                }
            }
        }, {
            "$sort": {
                "inDate": -1
            }
        }, {
            "$limit": 1
        }, {
            "$project": {
                "_id": 0
            }
        }]
        result = db[collection].aggregate(pip)
        res = []
        for r in result:
            # print(r)
            del r['inDate']
            if 'editDate' in r:
                del r['editDate']
            res.append(r)

        return res[0]

    def getbyDeviceTime(self, deviceTime, collection):
        db = self.client.ibuild_data
        td = datetime.strptime(deviceTime, "%Y-%m-%d %H:%M:%S")
        td = datetime.utcfromtimestamp(td.timestamp())
        # print(td)
        pip = [{
            "$match": {
                "deviceTime": {
                    "$eq": datetime(td.year, td.month, td.day, td.hour,
                                    td.minute, td.second)
                }
            }
        }, {
            "$sort": {
                "inDate": -1
            }
        }, {
            "$limit": 1
        }, {
            "$project": {
                "_id": 0
            }
        }]
        result = db[collection].aggregate(pip)
        res = []
        for r in result:
            # print(r)
            del r['inDate']
            del r['projectSysNo']
            if 'dataId' in r:
                del r['dataId']
            res.append(r)

        return res[0]

    def getbyParams(self, logitude, collection):
        db = self.client.ibuild_data
        # print(td)
        pip = [{
            "$match": {
                "longitude": logitude
            }
        }, {
            "$sort": {
                "inDate": -1
            }
        }, {
            "$limit": 1
        }, {
            "$project": {
                "_id": 0
            }
        }]
        result = db[collection].aggregate(pip)
        res = []
        for r in result:
            # print(r)
            del r['inDate']
            res.append(r)

        del res[0]['projectSysNo']
        return res[0]


if __name__ == "__main__":
    c = pymongo()

    res = c.getbyDeviceTime("2018-08-07 12:25:53", "env_monitor")
    # res = c.getbySourceId("ce9a25b1-e9fe-49a1-938e-18a89e91c0f0",
    # "process_task")
    print(res)

    pipline = [{
        "$match": {
            "deviceId": {
                "$in": ["20026-1"]
            },
            "inDate": {
                "$gt": datetime(2018, 7, 23)
            }
        }
    }, {
        "$sort": {
            "inDate": -1
        }
    }, {
        "$limit": 1
    }, {
        "$project": {
            "_id": 0
        }
    }]

    # res = c.aggregate(pipline, "env_monitor")
    """
    print(res)
    # print(res.key)
    print(res['deviceTime'].strftime("%Y-%m-%d %H:%M:%S"))
    print(res['inDate'].strftime("%Y-%m-%d %H:%M:%S.%f"))
    res['deviceTime'] = res['deviceTime'].strftime("%Y-%m-%d %H:%M:%S.%f")
    res['inDate'] = res['inDate'].strftime("%Y-%m-%d %H:%M:%S.%f")
    del res['inDate']
    print(json.dumps(res, indent=2, ensure_ascii=False))
    """
    # Group By
    pipeline = [{
        "$match": {
            "projectSysNo": 10112,
            "operationTime": {
                "$gt": datetime(2018, 4, 1)
            }
        }
    }, {
        "$group": {
            "_id": {
                "deviceId": "$deviceId",
                "projectSysNo": "$projectSysNo"
            },
            "count": {
                "$sum": 1
            },
            "avgpm10": {
                "$avg": "$pm10"
            }
        }
    }, {
        "$sort": {
            "_id.projectSysNo": 1,
            "_id.deviceId": 1
        }
    }, {
        "$project": {
            "deviceId": 1,
            "projectSysNo": 1,
            "count": 1,
            "avgpm10": 1
        }
    }]

    # c.aggregate(pipeline)

    # Simple Query
    pipline = [{
        "$match": {
            "projectSysNo": 10112,
            "operationTime": {
                "$gt": datetime(2018, 4, 1)
            }
        }
    }, {
        "$sort": {
            "operationTime": 1
        }
    }, {
        "$limit": 10
    }, {
        "$project": {
            "_id": 0,
            "sysNo": 1,
            "deviceId": 1,
            "projectSysNo": 1,
            "operationTime": 1,
            "pm10": 1
        }
    }]

    # c.aggregate(pipline)
