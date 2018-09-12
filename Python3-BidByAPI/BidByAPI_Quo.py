#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# # @Author: Bing.B.Yan <yanbin>
# @Date:   2016-12-02T17:04:50+08:00
# @Email:  Bing.B.Yan@yzw.cn
# @Last modified by:   yanbin
# @Last modified time: 2017-12-08T10:56:28+08:00

import json
import random
#  import urllib2
#  import cookielib
import time
import requests
import requests.packages.urllib3.util.ssl_
import os
from ConfirmSuccess import ConfirmSuccessOrders
from scrapy.selector import Selector
os.chdir(os.path.dirname(os.path.realpath(__file__)))
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
# xstr = lambda s: s or 0


def xstr(s):
    if s is True:
        return s
    else:
        return 0


# 环境配置
QA = {
    "loginUrl": "http://mall.yzw.cn.qa:8000",
    "VendorPortal": "http://mall.yzw.cn.qa:8000",
    "JCPortal": "http://portal.jc.yzw.cn.qa:8000"
}

PRE = {
    "loginUrl": "http://malltest.yzw.cn:16000",
    "VendorPortal": "http://malltest.yzw.cn:16000"
}

PRD = {
    "loginUrl": "https://mall.yzw.cn",
    "VendorPortal": "https://mall.yzw.cn"
}

PRDTest = {
    "loginUrl": "https://mall.yzw.cn:8081",
    "VendorPortal": "https://mall.yzw.cn:8081"
}


OrderList = []

# 登录
def login(url, user, password):
    try:
        cliid = requests.get(url)
        c     = requests.get(url + '/Login/LoginValidationCode', cookies=cliid.cookies)
        par   = '/Common/Login?account=' + user + '&password=' + password + '&verifycode=1000'
        d     = requests.post(url + par, cookies=c.cookies)
        return d.cookies, d.json()["Data"]["UserInfo"]["SupplierSysNo"], user
    except Exception:
        print(user, ": Login Fail!!!", d.text.encode('utf-8'))


# Exceptions
def CheckResponse(step, res, LoginInfo):
    resText = res.text
    #  print(resText)
    if "页面错误" in resText:
        e = Selector(text=resText).xpath('//ol/text()').extract()[0]
        # print(e)
        raise Exception(LoginInfo[2] + " : " + step, e)
    if res.json()["Success"] is not True:
        raise Exception(LoginInfo[2] + " : " + step + "Fail: ", res.text.encode('utf-8'))


# 签收招标公告
def Sign_up(VendorPortal, LoginInfo, TenderID):
    try:
        Cookies       = LoginInfo[0]
        SupplierSysNo = LoginInfo[1]
        # 签收
        SignAnnouncementPath = '/VendorPortal/Bidding/BidAction'
        SignAnno = {
            "action_type": "SignAnnouncement",
            "tender_id": str(TenderID),
            "supplier_id": SupplierSysNo
        }
        SignAnnoRes = requests.post(
            VendorPortal + SignAnnouncementPath, cookies=Cookies, data=SignAnno)
        # print(SignAnnoRes.text.encode('utf-8'))
        CheckResponse("签收招标公告：", SignAnnoRes, LoginInfo)

        # 由于数据库读写分离
        time.sleep(1)
        # 报名
        SignUpReq = {
            "attach": [],
            "action_type": "SignUp",
            "tender_id": str(TenderID),
            "supplier_id": SupplierSysNo
        }
        SignUpRes = requests.post(
            VendorPortal + SignAnnouncementPath, cookies=Cookies, data=SignUpReq)
        # print(SignUpRes.text.encode('utf-8'))
        CheckResponse("报名：", SignUpRes, LoginInfo)

        # if SignUpRes.json()["Success"] != True:
        #     raise ValueError("SignUp Fail...", SignUpRes.text.encode('utf-8'))
    except Exception as e:
        print(e)

def SignCalibration(VendorPortal, LoginInfo, TenderID):
    try:
        Cookies        = LoginInfo[0]
        SupplierSysNo  = LoginInfo[1]
        SignTenderPath = '/VendorPortal/Bidding/BidAction'
        SignTenderReq  = {
            "action_type": "ViewCalibration",
            "tender_id": str(TenderID),
            "supplier_id": SupplierSysNo
        }
        SignTenderRes = requests.post(
            VendorPortal + SignTenderPath, cookies=Cookies, data=SignTenderReq)
        CheckResponse("签收招标结果：", SignTenderRes, LoginInfo)
        # if SignTenderRes.json()["Success"] != True:
        #     raise ValueError( "SignTender Fail!!!" , SignTenderRes.text.encode('utf-8'))
    except Exception as e:
        print(e)

# 签收招标文件
def SignTender(VendorPortal, LoginInfo, TenderID):
    try:
        Cookies        = LoginInfo[0]
        SupplierSysNo  = LoginInfo[1]
        SignTenderPath = '/VendorPortal/Bidding/BidAction'
        SignTenderReq  = {
            "action_type": "SignTender",
            "tender_id": str(TenderID),
            "supplier_id": SupplierSysNo
        }
        SignTenderRes = requests.post(
            VendorPortal + SignTenderPath, cookies=Cookies, data=SignTenderReq)
        CheckResponse("签收招标文件：", SignTenderRes, LoginInfo)
        # if SignTenderRes.json()["Success"] != True:
        #     raise ValueError( "SignTender Fail!!!" , SignTenderRes.text.encode('utf-8'))
    except Exception as e:
        print(e)

# 签收招标文件
def CreateOrder(VendorPortal, LoginInfo, TenderID):
    try:
        Cookies        = LoginInfo[0]
        SupplierSysNo  = LoginInfo[1]
        SignTenderPath = '/VendorPortal/Bidding/CreateOrder'
        SignTenderReq  = {
            "TenderSysNo": str(TenderID),
            "SupplierSysNo": SupplierSysNo
            }
        SignTenderRes = requests.post(
            VendorPortal + SignTenderPath, cookies=Cookies, data=SignTenderReq)
        # print(SignTenderRes.text)
        CheckResponse("创建投标保证金支付订单：", SignTenderRes, LoginInfo)
        return SignTenderRes.json()['Data']['SysNo']
        # if SignTenderRes.json()["Success"] != True:
        #     raise ValueError( "SignTender Fail!!!" , SignTenderRes.text.encode('utf-8'))
    except Exception as e:
        print(e)


# 获取[我的投标文件]
def LoadBiddingFile(url, LoginInfo, TenderID):
    try:
        Cookies         = LoginInfo[0]
        SupplierSysNo   = LoginInfo[1]
        LoadBiddingPath = '/VendorPortal/bidding/LoadBiddingFile?tenderSysNo=' + \
            str(TenderID) + '&supplierSysNo=' + str(SupplierSysNo)
        beginTime       = time.time()
        BiddingFile     = requests.post(url + LoadBiddingPath, cookies=Cookies)
        print(LoginInfo[2], 'LoadBiddingFile in: ', time.time() - beginTime, ' seconds.')
        CheckResponse("LoadBiddingFile", BiddingFile, LoginInfo)
        # a = BiddingFile.json()
        #  print(json.dumps(a, indent=4, sort_keys=True))
        return BiddingFile.json()
    except Exception as e:
        print(e)


def listappend(l, id, key, value):
    return l.append({"id": id, key: value})


# 构建投标清单
def BuildBidList(BidL):
    ListContentData = []
    ProductDate = "2017-01-01"
    columnData = BidL['columnData']
    BidCol = [c for c in columnData
              if c['enableEdit'] is True
              and c['columnName'] != 'SordIndex']
    # print('BuildBidList=============')
    # print(json.dumps(BidCol,indent=4))
    for data in BidL["data"]:
        # if abs(int(float(xstr(data["QuotedPrice"]))))>0:
        if "QuotedPrice" in data and abs(int(float(xstr(data["QuotedPrice"])))) > 0:
            for col in BidCol:
                QuotedPrice = int(float(xstr(data["QuotedPrice"]))) - float(random.randint(0, 10))/100
                if col['columnType'] == "date":
                    listappend(ListContentData, data["id"],
                               col['columnName'], ProductDate)
                elif col['isPercent'] is True:
                    listappend(ListContentData, data["id"], col['columnName'],
                               random.randint(0, 100)/100)
                else:
                    listappend(ListContentData, data["id"], col['columnName'], QuotedPrice)
            if "children" in data:
                for cdata in data["children"]:
                    for col in BidCol:
                        QuotedPrice = int(float(xstr(cdata["QuotedPrice"]))) - random.randint(0, 10)
                        if col['columnType'] == "date":
                            listappend(ListContentData, cdata["id"],
                                       col['columnName'], ProductDate)
                        elif col['isPercent'] is True:
                            listappend(ListContentData, cdata["id"], col['columnName'],
                                    random.randint(0, 100)/100)
                        else:
                            listappend(ListContentData, cdata["id"], col['columnName'], QuotedPrice)
                    # cQuotedPrice = int(float(xstr(cdata["QuotedPrice"])))-random.randint(0, 10)
                    # listappend(ListContentData,cdata["id"],"QuotedPrice",cQuotedPrice)
                    # listappend(ListContentData,data["id"], "ProductDate", ProductDate)

        else:
            for col in BidCol:
                QuotedPrice = float(random.randint(0,1000))/100
                if col['columnType'] == "date":
                    listappend(ListContentData, data["id"],
                               col['columnName'], ProductDate)
                elif col['isPercent'] is True:
                    listappend(ListContentData, data["id"], col['columnName'],
                                    random.randint(0, 100)/100)
                else:
                    listappend(ListContentData, data["id"], col['columnName'], QuotedPrice)
            # QuotedPrice = random.randint(-50, 100)
            # listappend(ListContentData,data["id"], "QuotedPrice", QuotedPrice)
            # listappend(ListContentData,data["id"], "ProductDate", ProductDate)
            if "children" in data:
                for cdata in data["children"]:
                    for col in BidCol:
                        QuotedPrice = random.randint(50, 200)
                        if col['columnType'] == "date":
                            listappend(ListContentData, cdata["id"],
                                       col['columnName'], ProductDate)
                        elif col['isPercent'] is True:
                            listappend(ListContentData, cdata["id"], col['columnName'],
                                       random.randint(0, 100)/100)
                        else:
                            listappend(ListContentData, cdata["id"], col['columnName'], QuotedPrice)
                    # cQuotedPrice = random.randint(-50, 100)
                    # listappend(ListContentData,cdata["id"],"QuotedPrice",cQuotedPrice)
                    # listappend(ListContentData,cdata["id"],"ProductDate",ProductDate)
    return ListContentData


# 构建税前价清单
def Build_sqj_BidList(BidL):
    ListContentData = []
    for data in BidL["data"]:
        if abs(int(float(xstr(data["sqj"])))) > 0 or abs(int(float(xstr(data["QuotedPrice"])))) > 0:
            sqj = int(float(xstr(data["sqj"]))) - random.randint(0, 10)
            zz001 = float(random.randint(0, 17))
            QuotedPrice = round(float(sqj) * (1 + zz001 / 100), 2)

            listappend(ListContentData, data["id"], "sqj", sqj)
            listappend(ListContentData, data["id"], "QuotedPrice", QuotedPrice)
            listappend(ListContentData, data["id"], "zz001", zz001)

            if "children" in data:
                for cdata in data["children"]:
                    csqj = int(float(xstr(cdata["sqj"]))) - random.randint(0, 10)
                    czz001 = float(random.randint(0, 17))
                    cQuotedPrice = round(float(sqj) * (1 + czz001 / 100), 2)

                    listappend(ListContentData, cdata["id"], "sqj", csqj)
                    listappend(ListContentData, cdata["id"], "QuotedPrice", cQuotedPrice)
                    listappend(ListContentData, cdata["id"], "zz001", czz001)

        else:
            sqj = random.randint(-50, 100)
            zz001 = float(random.randint(0, 17))
            QuotedPrice = round(float(sqj) * (1 + zz001 / 100), 2)

            listappend(ListContentData, data["id"], "sqj", sqj)
            listappend(ListContentData, data["id"], "QuotedPrice", QuotedPrice)
            listappend(ListContentData, data["id"], "zz001", zz001)

            if "children" in data:
                for cdata in data["children"]:
                    csqj = random.randint(-50, 100)
                    czz001 = float(random.randint(0, 17))
                    cQuotedPrice = round(float(sqj) * (1 + czz001 / 100), 2)

                    listappend(ListContentData, cdata["id"], "sqj", csqj)
                    listappend(ListContentData, cdata["id"], "QuotedPrice", cQuotedPrice)
                    listappend(ListContentData, cdata["id"], "zz001", czz001)
    return ListContentData


# 保存投标清单
def SaveBidList(VendorPortal, LoginInfo, TenderID):
    #  设置商品价格,并且保存清单
    try:
        BidList = LoadBiddingFile(VendorPortal, LoginInfo, TenderID)
        # BidAction Request Data:
        # {
        #     "doesBid": true,
        #     "dataString": "\n    {
        #         \"tender_id\":\"34543\",\n
        #         \"content\":[{
        #             \"id\":59307,\n
        #             \"data\":[{
        #                 \"id\":1,\n    \"QuotedPrice\":\"69\"},\n
        #                 {\"id\":1,\n    \"Description\":\"59\"
        #                     }]
        #                 }]}\n"
        # }
        Cookies = LoginInfo[0]
        # SupplierSysNo = LoginInfo[1]
        for Bid in BidList["Data"]["biddingList"]["bid_lists"]:
            t = {
                "doesBid": True,
                "dataString": ""
            }
            TenderList = {
                "tender_id": str(TenderID),
                "content": []
            }
            ListContent = [
                {
                    "id": Bid["id"],
                    "data": []
                }
            ]
            BidL = Bid["data"].encode('utf-8')
            BidL = json.loads(BidL)

            # print str(json.dumps(BidL))
            # 判断清单类型，使用对应的方法构建投标清单
            if "sqj" in BidL["data"][0]:
                ListContentData = Build_sqj_BidList(BidL)
            else:
                ListContentData = BuildBidList(BidL)

            # print(json.dumps(ListContentData,indent=4, ensure_ascii=False))
            ListContent[0]["data"] = ListContentData
            TenderList["content"]  = ListContent
            t["dataString"]        = str(json.dumps(TenderList))
            # Bid["data"] = json.dumps(BidL)
            data                   = t
            beginTime              = time.time()
            SaveBidListPath        = '/VendorPortal/Bidding/SaveBiddingList'
            SaveBidList            = requests.post(
                VendorPortal + SaveBidListPath, cookies=Cookies, data=data)
            print(LoginInfo[2], 'SaveBidList in: ', time.time() - beginTime, ' seconds.')
            # print SaveBidList.text.encode('utf-8')
            CheckResponse("保存投标清单：", SaveBidList, LoginInfo)
    except Exception as e:
        print(e)


# 投标
def BiddingAction(VendorPortal, LoginInfo, TenderID):
    try:
        Cookies           = LoginInfo[0]
        SupplierSysNo     = LoginInfo[1]
        BiddingActionPath = '/VendorPortal/Bidding/BidAction'
        data              = {
            "remark": "",
            "action_type": "Bid",
            "tender_id": str(TenderID),
            "supplier_id": SupplierSysNo
        }
        BiddingActionRes  = requests.post(
            VendorPortal + BiddingActionPath, cookies=Cookies, data=data)
        CheckResponse("投标：", BiddingActionRes, LoginInfo)
    except Exception as e:
        print(e)


# 投标 Main
def Bid_mainSingleUser(username, pwd, site, TenderID):
    # beginTime    = time.time()
    loginUrl     = site['loginUrl']
    VendorPortal = site['VendorPortal']
    # print "Bid_main: ",loginUrl,VendorPortal
    ibtime       = time.time()

    user         = username
    password     = pwd
    LoginInfo    = login(loginUrl, user, password)     # 登录
    # SignTender(VendorPortal, LoginInfo, TenderID)  # 签收招标文件
    # CreateOrder(VendorPortal, LoginInfo, TenderID)  # 签收招标文件
    SaveBidList(VendorPortal,   LoginInfo, TenderID)  # 保存投标清单
    BiddingAction(VendorPortal, LoginInfo, TenderID)  # 投标
    print(user, ' Bidding Finish in:', time.time() - ibtime, ' seconds.\n')


def SigntenderFile_mainSingleUser(username, pwd, site, TenderID):
    # beginTime    = time.time()
    loginUrl     = site['loginUrl']
    VendorPortal = site['VendorPortal']
    # print "Bid_main: ",loginUrl,VendorPortal
    ibtime       = time.time()

    user         = username
    password     = pwd
    LoginInfo    = login(loginUrl, user, password)     # 登录
    SignTender(VendorPortal, LoginInfo, TenderID)  # 签收招标文件
    OrderNo = CreateOrder(VendorPortal, LoginInfo, TenderID)  # 签收招标文件
    OrderList.append(OrderNo)
    ConfirmSuccessOrders(site, OrderList)
    # SaveBidList(VendorPortal, LoginInfo, TenderID)  # 保存投标清单
    # BiddingAction(VendorPortal, LoginInfo, TenderID)  # 投标
    print(user, ' SigntenderFile Finish in:', time.time() - ibtime, ' seconds.\n')


def ViewCalibration_mainSingleUser(username, pwd, site, TenderID):
    # beginTime    = time.time()
    loginUrl     = site['loginUrl']
    VendorPortal = site['VendorPortal']
    # print "Bid_main: ",loginUrl,VendorPortal
    ibtime       = time.time()

    user         = username
    password     = pwd
    LoginInfo    = login(loginUrl, user, password)     # 登录
    SignCalibration(VendorPortal, LoginInfo, TenderID)  # 签收招标文件
    OrderNo = CreateOrder(VendorPortal, LoginInfo, TenderID)  # 签收招标文件
    OrderList.append(OrderNo)
    # ConfirmSuccessOrders(site, OrderList)
    # SaveBidList(VendorPortal, LoginInfo, TenderID)  # 保存投标清单
    # BiddingAction(VendorPortal, LoginInfo, TenderID)  # 投标
    print(user, ' Bidding Finish in:', time.time() - ibtime, ' seconds.\n')


# 报名 Main
def SignUP_mainSingleUser(username, pwd, site, TenderID):
    # beginTime    = time.time()
    loginUrl     = site['loginUrl']
    VendorPortal = site['VendorPortal']
    # print "SignUP_main: ",loginUrl,VendorPortal
    ibtime       = time.time()

    user         = username
    password     = pwd
    LoginInfo    = login(loginUrl, user, password)    # 登录
    Sign_up(VendorPortal, LoginInfo, TenderID)   # 签收招标文件,并且报名
    print(user, ' SignUP Finish in:', time.time() - ibtime, ' seconds.\n')


# 投标 Main
def Bid_main(userList, site, TenderID):
    beginTime    = time.time()
    loginUrl     = site['loginUrl']
    VendorPortal = site['VendorPortal']
    # print "Bid_main: ",loginUrl,VendorPortal
    with open(userList, 'r') as f:
        my_list = f.readlines()
        for i in my_list:
            if len(i) > 0:
                ibtime    = time.time()
                my_data   = i.split(',')
                user      = my_data[0]
                password  = my_data[1]
                LoginInfo = login(loginUrl, user, password)     # 登录
                SignTender(VendorPortal, LoginInfo, TenderID)  # 签收招标文件
                CreateOrder(VendorPortal, LoginInfo, TenderID)  # 创建保证金支付订单
                SaveBidList(VendorPortal, LoginInfo, TenderID)  # 保存投标清单
                BiddingAction(VendorPortal, LoginInfo, TenderID)  # 投标
                print(user, ' Bidding Finish in:', time.time() - ibtime, ' seconds.\n')
    print('Finish All in: ', time.time() - beginTime, 'seconds.')


# 报名 Main
def SignUP_main(userList, site, TenderID):
    beginTime    = time.time()


if __name__ == '__main__':
    # SignUP_main('./user.txt',                PRD,       690153)
    # Bid_main('./user.txt',                   QA,        35213)
    # Bid_main('./user.txt',                   PRD,       702579)
    # login('https://mall.yzw.cn',             'sup100',  '111111')
    # SignUP_mainSingleUser('sup111',          '111111',  QA,        42691)
    # Bid_mainSingleUser('sup100',             '111111',  QA,        36376)
    # SigntenderFile_mainSingleUser('sup115',  '111111',  QA,        42711)
    Bid_mainSingleUser('sup101',             '111111',  PRD,        1100389)
    # ViewCalibration_mainSingleUser('sup100',   '111111',  QA,        42701)
