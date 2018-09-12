# coding=utf-8
# # @Author: Bing.B.Yan <yanbin>
# @Date:   2016-12-02T17:04:50+08:00
# @Email:  Bing.B.Yan@yzw.cn
# @Last modified by:   yanbin
# @Last modified time: 2017-01-12T17:45:37+08:00

import json
import random
import time
import requests
import requests.packages.urllib3.util.ssl_
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
xstr = lambda s: s or 0

# 登录
def login(url, user, password):
    try:
        c = requests.get(url + '/Common/LoginValidationCode')
        par = '/Login/Login?account=' + user + '&password=' + password + '&verifycode=-1'
        d = requests.post(url + par, cookies=c.cookies)
        return d.cookies, d.json()["Data"]["UserInfo"]["SupplierSysNo"]
    except Exception:
        print (user, ": Login Fail!!!", d.text.encode('utf-8'))

# 生成支付订单
def CreateOrder(url, username, pwd):
    try:
        login_info = login(url, username, pwd)
        cookies = login_info[0]
        OrderPath = '/SSL/Yunmi/CreateOrder'
        CreateReq = {
            "productSysNo": "10013",
            "quantity": '1000',
        }
        CreateOrderRes = requests.post(
            url + OrderPath, cookies=cookies, data=CreateReq)
        print (CreateOrderRes._content)
        # if SignTenderRes.json()["Success"] != True:
        #     raise ValueError( "SignTender Fail!!!" , SignTenderRes.text.encode('utf-8'))
    except Exception as e:
        print ("SignTender Fail!!!")
# 签收招标公告
def Sign_up(VendorPortal, LoginInfo, TenderID):
    try:
        Cookies = LoginInfo[0]
        SupplierSysNo = LoginInfo[1]

        # 签收
        SignAnnouncementPath = '/VendorPortal/Bidding/BidAction'
        SignAnno = {
            "action_type": "SignAnnouncement",
            "tender_id": str(TenderID),
            "supplier_id": SupplierSysNo
        }
        # print SignAnno,VendorPortal+SignAnnouncementPath
        SignAnnoRes = requests.post(
            VendorPortal + SignAnnouncementPath, cookies=Cookies, data=SignAnno)

        # print SignAnnoRes.text.encode('utf-8')

        if SignAnnoRes.json()["Success"] != True:
            raise ValueError("SignAnno Fail...",
                             SignAnnoRes.text.encode('utf-8'))
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
        # print SignUpRes.text.encode('utf-8')
        if SignUpRes.json()["Success"] != True:
            raise ValueError("SignUp Fail...", SignUpRes.text.encode('utf-8'))

    except Exception as e:
        print ("Sign_up Fail!!!",e)

# 签收招标文件
def SignTender(VendorPortal, LoginInfo, TenderID):
    try:
        Cookies = LoginInfo[0]
        SupplierSysNo = LoginInfo[1]
        SignTenderPath = '/VendorPortal/Bidding/BidAction'
        SignTenderReq = {
            "action_type": "SignTender",
            "tender_id": str(TenderID),
            "supplier_id": SupplierSysNo
        }
        SignTenderRes = requests.post(
            VendorPortal + SignTenderPath, cookies=Cookies, data=SignTenderReq)
        # if SignTenderRes.json()["Success"] != True:
        #     raise ValueError( "SignTender Fail!!!" , SignTenderRes.text.encode('utf-8'))
    except Exception as e:
        print ("SignTender Fail!!!")

# 获取[我的投标文件]
def LoadBiddingFile(url,  LoginInfo, TenderID):
    try:
        Cookies = LoginInfo[0]
        SupplierSysNo = LoginInfo[1]
        LoadBiddingPath = '/VendorPortal/bidding/LoadBiddingFile?tenderSysNo=' + \
            str(TenderID) + '&supplierSysNo=' + str(SupplierSysNo)
        beginTime = time.time()
        BiddingFile = requests.post(url + LoadBiddingPath, cookies=Cookies)
        print ('LoadBiddingFile in: ', time.time() - beginTime, ' seconds.')
        if BiddingFile.status_code != 200:
            raise ValueError("LoadBiddingFile Fail!!!",
                             BiddingFile.status_code)
        return BiddingFile.json()
    except Exception as e:
        print ("LoadBiddingFile Fail!!!")

def listappend(l,id,key,value):
    return l.append({"id":id,key:value})

def BuildBidList(BidL):
    ListContentData = []
    for data in BidL["data"]:
        if abs(int(float(xstr(data["QuotedPrice"]))))>0:
            #sqj = int(float(xstr(data["sqj"])))-random.randint(0, 10)
            zz001 = float(random.randint(0, 17))
            QuotedPrice = random.randint(0, 10)

            #listappend(ListContentData,data["id"],"sqj",sqj)
            listappend(ListContentData,data["id"],"QuotedPrice",QuotedPrice)
            #listappend(ListContentData,data["id"],"zz001",zz001)

            if "children" in data:
                for cdata in data["children"]:
                    #csqj = int(float(xstr(cdata["sqj"])))-random.randint(0, 10)
                    czz001 = float(random.randint(0, 17))
                    cQuotedPrice = random.randint(0, 10)

                    #listappend(ListContentData,data["id"],"sqj",csqj)
                    listappend(ListContentData,data["id"],"QuotedPrice",cQuotedPrice)
                    #listappend(ListContentData,data["id"],"zz001",czz001)

        else:
            sqj = random.randint(0, 10)
            zz001 = float(random.randint(0, 17))
            QuotedPrice = random.randint(0, 10)

            #listappend(ListContentData,data["id"], "sqj", sqj)
            listappend(ListContentData,data["id"], "QuotedPrice", QuotedPrice)
            #listappend(ListContentData,data["id"], "zz001", zz001)

            if "children" in data:
                for cdata in data["children"]:
                    csqj = random.randint(0, 10)
                    czz001 = float(random.randint(0, 17))
                    cQuotedPrice = random.randint(0, 10)

                    #listappend(ListContentData,cdata["id"], "sqj", csqj)
                    listappend(ListContentData,cdata["id"], "QuotedPrice", cQuotedPrice)
                    #listappend(ListContentData,cdata["id"], "zz001", czz001)
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
        SupplierSysNo = LoginInfo[1]
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
            ListContentData = BuildBidList(BidL)
            ListContent[0]["data"] = ListContentData
            TenderList["content"] = ListContent
            t["dataString"] = str(json.dumps(TenderList))
            # Bid["data"] = json.dumps(BidL)
            # print t
            data = t
            # SaveBiddingList

            beginTime = time.time()
            SaveBidListPath = '/VendorPortal/Bidding/SaveBiddingList'
            SaveBidList = requests.post(
                VendorPortal + SaveBidListPath, cookies=Cookies, data=data)

            print ('SaveBidList in: ', time.time() - beginTime, ' seconds.')
            # print SaveBidList.text.encode('utf-8')
            if SaveBidList.json()["Success"] != True:
                raise ValueError("Response Code: ",
                                 SaveBidList.text.encode('utf-8'))
    except Exception as e:
        print ("SetBidPrice Fail!!!" ,e)

# 投标
def BiddingAction(VendorPortal, LoginInfo, TenderID):
    try:
        Cookies = LoginInfo[0]
        SupplierSysNo = LoginInfo[1]
        BiddingActionPath = '/VendorPortal/Bidding/BidAction'
        data = {
            "remark": "",
            "action_type": "Bid",
            "tender_id": str(TenderID),
            "supplier_id": SupplierSysNo
        }
        BiddingActionRes = requests.post(
            VendorPortal + BiddingActionPath, cookies=Cookies, data=data)
        if BiddingActionRes.json()["Success"] != True:
            raise ValueError("Response Code: ",
                             BiddingActionRes.text.encode('utf-8'))
    except Exception as e:
        print ("BiddingAction Fail!!!", BiddingActionRes.text.encode('utf-8'))

# 投标 Main
def Bid_main(userList, site, TenderID):
    beginTime = time.time()
    loginUrl = site['loginUrl']
    VendorPortal = site['VendorPortal']
    # print "Bid_main: ",loginUrl,VendorPortal

    f = open(userList, 'r')
    my_list = f.readlines()
    for i in my_list:
        if len(i)>0:
            ibtime = time.time()
            my_data = i.split(',')
            user = my_data[0]
            password = my_data[1]
            LoginInfo = login(loginUrl, user, password)     # 登录
            SignTender(VendorPortal, LoginInfo, TenderID)  # 签收招标文件
            SaveBidList(VendorPortal, LoginInfo, TenderID)  # 保存投标清单
            BiddingAction(VendorPortal, LoginInfo, TenderID)  # 投标
            print (user, ' Bidding Finish in:',time.time() - ibtime, ' seconds.\n')
    print ('Finish All in: ', time.time() - beginTime, 'seconds.')

# 报名 Main
def SignUP_main(userList, site, TenderID):
    beginTime = time.time()
    loginUrl = site['loginUrl']
    VendorPortal = site['VendorPortal']
    # print "SignUP_main: ",loginUrl,VendorPortal

    f = open(userList, 'r')
    my_list = f.readlines()
    for i in my_list:
        if len(i)>0:
            ibtime = time.time()
            my_data = i.split(',')
            user = my_data[0]
            password = my_data[1]
            LoginInfo = login(loginUrl, user, password)    # 登录
            Sign_up(VendorPortal, LoginInfo, TenderID)   # 签收招标文件,并且报名
            print (user, ' SignUP Finish in:', time.time() - ibtime, ' seconds.\n')
    print ('Finish All in: ', time.time() - beginTime, ' seconds.')




if __name__ == '__main__':
    QA = {
        "loginUrl": "http://mall.yzw.cn.qa:8002",
        "VendorPortal": "http://mall.yzw.cn.qa:8002"
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
    #  SignUP_main('./user.txt', PRDTest, 721333)
    #Bid_main('user_prd', PRD, 764359)
    SignUP_main('user_prd', PRDTest, 894047)
    #CreateOrder("http://mall.yzw.cn.qa:8000", 'sup129', '111111')
    #login('https://jc.yzw.cn','sup100','111111')
