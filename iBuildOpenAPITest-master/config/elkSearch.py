#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import datetime
import time
from .AppConfig import ENV

headers = {"content-type": "application/x-ndjson", "kbn-version": "5.5.0"}
if ENV['Env'] == 'QA':
    url = "http://172.16.0.239:5601/elasticsearch/_msearch"
if ENV['Env'] == 'PRD':
    url = "http://192.168.110.23:5601/elasticsearch/_msearch"
ind = {
    "index": ["logstash-ibuild-data-log*"],
    "ignore_unavailable": True,
    "preference": 1532426321942
}


def elkD(q, d=""):
    """
    设备：根据DeviceTime查询elk
    软件：根据dataContent，进行guid模糊查询
    """
    # sleep 5 秒 等数据处理完成
    q = str(q)
    # time.sleep(5)
    qs = "dataContent:(\"" + q + "\")"
    if len(d) > 0:
        qs = qs + " AND method:" + d
    """
    if q == "":
        qs = "*"
    else:
        td = datetime.datetime.strptime(q, "%Y-%m-%d %H:%M:%S").timetuple()
        dataTimeStamp = int(time.mktime(td)) * 1000
        qs = "dataType:1 AND deviceTime:" + str(dataTimeStamp)
    """
    query = {
        "size": 5,
        "sort": [{
            "@timestamp": {
                "order": "desc",
                "unmapped_type": "boolean"
            }
        }],
        "query": {
            "bool": {
                "must": [{
                    "query_string": {
                        "analyze_wildcard": True,
                        "query": qs
                    }
                }, {
                    "range": {
                        "@timestamp": {
                            "gte": int(
                                (datetime.datetime.now() - datetime.timedelta(
                                    minutes=15)).timestamp() * 1000),
                            "lte":
                            int(datetime.datetime.now().timestamp() * 1000),
                            "format": "epoch_millis"
                        }
                    }
                }]
            }
        }
    }

    query = json.dumps(ind) + "\n" + json.dumps(query) + "\n"
    res = requests.post(url, data=query, headers=headers)

    return res


def elkDevice(q, d=""):
    """
    设备：根据DeviceTime查询elk
    软件：根据dataContent，进行guid模糊查询
    """
    i = 0
    while i <= 10:
        time.sleep(1)
        res = elkD(q, d)
        # print(res.json())
        # print(i)

        if len(res.json()['responses'][0]['hits']['hits']) > 0:
            r = res.json()['responses'][0]['hits']['hits']
            if "uploadStatus" in r[0]['_source']:
                return r[0]['_source']
        i += 1


def elkS(q, P=""):
    """
    设备：根据DeviceTime查询elk
    软件：根据dataContent，进行guid模糊查询
    """
    # sleep 5 秒 等数据处理完成
    # time.sleep(5)

    qs = "dataContent:(\"" + q + "\")"
    if len(P) > 0:
        qs = qs + " AND method:" + P
    query = {
        "size": 5,
        "sort": [{
            "@timestamp": {
                "order": "desc",
                "unmapped_type": "boolean"
            }
        }],
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "analyze_wildcard": True,
                            # "query": "dataType:1"
                            "query": qs
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": int(
                                    (datetime.datetime.now() -
                                     datetime.timedelta(minutes=1)).timestamp()
                                    * 1000),
                                "lte": int(datetime.datetime.now().timestamp()
                                           * 1000),
                                "format": "epoch_millis"
                            }
                        }
                    }
                ]
            }
        }
    }

    query = json.dumps(ind) + "\n" + json.dumps(query) + "\n"
    res = requests.post(url, data=query, headers=headers)
    return res


def elkSoftware(q, P=""):
    """
    设备：根据DeviceTime查询elk
    软件：根据dataContent，进行guid模糊查询
    """
    i = 0
    while i <= 10:
        time.sleep(1)
        res = elkS(q, P)
        # print(res.json())
        # print(i)

        if len(res.json()['responses'][0]['hits']['hits']) > 0:
            r = res.json()['responses'][0]['hits']['hits']
            if "uploadStatus" in r[0]['_source']:
                return r[0]['_source']
        i += 1
    """
    pdataTime = json.loads(r[0]['_source']['dataContent'])['deviceTime']
    td = datetime.datetime.strptime(pdataTime, "%Y-%m-%d %H:%M:%S").timetuple()
    dataTimeStamp = int(time.mktime(td)) * 1000
    print(dataTimeStamp)
    print(json.dumps(r, indent=2, ensure_ascii=False))
    print(json.dumps(
        json.loads(r[0]['_source']['dataContent']),
        indent=2,
        ensure_ascii=False))
    dataTime = json.loads(r[0]['_source']['dataContent'])['deviceTime']
    td = datetime.datetime.strptime(dataTime, "%Y-%m-%d %H:%M:%S").timetuple()
    dataTimeStamp = int(time.mktime(td)) * 1000
    """
    # return json.loads(r[0]['_source']['dataContent'])
    # return r


def elkP(q, m):
    """
    设备：根据DeviceTime查询elk
    软件：根据dataContent，进行guid模糊查询
    """
    # sleep 5 秒 等数据处理完成
    q = str(q)
    # time.sleep(5)
    qs = "dataContent:(\"" + q + "\") AND method:" + m

    query = {
        "size": 5,
        "sort": [{
            "@timestamp": {
                "order": "desc",
                "unmapped_type": "boolean"
            }
        }],
        "query": {
            "bool": {
                "must": [{
                    "query_string": {
                        "analyze_wildcard": True,
                        "query": qs
                    }
                }, {
                    "range": {
                        "@timestamp": {
                            "gte": int(
                                (datetime.datetime.now() - datetime.timedelta(
                                    minutes=1)).timestamp() * 1000),
                            "lte":
                            int(datetime.datetime.now().timestamp() * 1000),
                            "format": "epoch_millis"
                        }
                    }
                }]
            }
        }
    }

    query = json.dumps(ind) + "\n" + json.dumps(query) + "\n"
    res = requests.post(url, data=query, headers=headers)

    return res


def elkParams(q, m):
    """
    设备：根据DeviceTime查询elk
    软件：根据dataContent，进行guid模糊查询
    """
    i = 0
    while i <= 10:
        time.sleep(1)
        res = elkD(q, m)
        # print(res.json())

        if len(res.json()['responses'][0]['hits']['hits']) > 0:
            r = res.json()['responses'][0]['hits']['hits']
            if "uploadStatus" in r[0]['_source']:
                return r[0]['_source']
        i += 1


if __name__ == "__main__":
    # res = elkSearch(1, 1532606064000)
    # res = elkSoftware("89e4a0d5-6555-4ca5-919a-66c56de5a9de")
    res = elkDevice("2018-08-07 12:25:53", 'OPENAPI')
    print(res)
    # 1532339992000
