#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json

# 环境配置
QA = {
    "loginUrl": "http://mall.yzw.cn.qa:8001",
    "JCPortal": "http://portal.jc.yzw.cn.qa:8001"
}

Orders = [100002503
,100002502
,100002501
,100002500
,100002499
,100002498
,100002497
,100002496
,100002495
,100002494
,100002493
,100002492
,100002491
,100002490
,100002489
,100002488
,100002487
,100002486
,100002485
,100002484] 

def login(url, user, password):
    try:
        cliid = requests.get(url)
        c     = requests.get(url + '/Login/LoginValidationCode', cookies=cliid.cookies)
        par   = '/Common/Login?account=' + user + '&password=' + password + '&verifycode=1000'
        d     = requests.post(url + par, cookies=c.cookies)
        return d.cookies
    except Exception:
        print(user, ": Login Fail!!!", d.text.encode('utf-8'))


def ConfirmSuccessOrders(site, Orders):
    loginUrl     = site['loginUrl']
    JCPortal = site['JCPortal']
    Path = '/OperationMgt/TenderBondPayOrder/ConfirmSuccess'

    user         = 'binga'
    password     = '111111'
    LoginInfo    = login(loginUrl, user, password)    # 登录

    for o in Orders:
        if o :
            ReqData = {
                "SysNo":o,
                "ConfirmMemo":"Confirm by script",
                "PayDate":"2018-01-23 17:46:33"
            }

            req = requests.post(JCPortal+Path,
                                data = ReqData,
                                cookies = LoginInfo)
            # print(req.text)


if __name__ == "__main__":
    ConfirmSuccessOrders(QA, Orders)
