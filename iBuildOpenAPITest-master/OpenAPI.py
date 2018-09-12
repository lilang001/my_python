#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import hashlib
from datetime import datetime
from config import AppConfig

appid = AppConfig.ENV['Code']
appsecret = AppConfig.ENV['Key']
url = AppConfig.ENV['Url']


def OpenAPI(p_appid=appid,
            httpmethod='post',
            method='',
            data='',
            p_appsecret=appsecret,
            p_format='json',
            p_version="1.0",
            p_time=None):
    # url = "http://api.mall.yzw.cn.qa:8003/open.api"

    if p_time is None:
        reqtime = datetime.now().strftime("%Y%m%d%H%M%S")
    else:
        reqtime = p_time
    appid = "appid=" + p_appid + "&"
    format = "format=" + p_format + "&"
    rmethod = "method=" + method + "&"
    Nonce = "nonce=123543&"
    Timestamp = "timestamp=" + reqtime + "&"
    Version = "version=" + p_version + "&"
    Data = "data=" + data + "&"
    appsecret = "appsecret=" + p_appsecret

    par = appid + \
        Data +\
        format +\
        rmethod +\
        Nonce +\
        Timestamp +\
        Version +\
        appsecret

    sign = hashlib.md5(par.lower().encode('utf-8')).hexdigest()

    # print(sign)

    # print(f" \nMethod: {method} \nURL: {url} \nUri:{par} \nHttpMethod: {httpmethod} ")
    if httpmethod == 'get':
        res = requests.get(url + par + "&sign=" + sign)
    elif httpmethod == 'post':
        d = {
            "appid": p_appid,
            "format": p_format,
            "method": method,
            "nonce": '123543',
            "timestamp": Timestamp.split('=')[1].replace('&', ''),
            "version": p_version,
            "data": data,
            "appsecret": p_appsecret,
            "sign": sign
        }
        # print(json.dumps(d,indent=4,ensure_ascii=False))
        res = requests.post(
            url,
            data=d,
            headers={"Content-Type": "application/x-www-form-urlencoded"})
    return res
