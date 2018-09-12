# coding=utf-8
#!/usr/bin/env python

# @Author: Bing.B.Yan <yanbin>
# @Date:   2016-07-13T20:54:08+08:00
# @Email:  Bing.B.Yan@yzw.cn
# @Last modified by:   yanbin
# @Last modified time: 2017-01-04T15:02:10+08:00

from pymysql import connect
import json

xstr = lambda s: s or 0
def GetBid(TenderSysNo):
    GetBidSql = """
        SELECT Top(1000) c.[Order],D.SupplierName,b.SupplierSysNo,b.ListValue
        FROM TenderList A WITH(nolock)
        INNER JOIN TenderListTable B WITH(nolock)
        ON a.SysNo = b.TenderListSysNo
        INNER JOIN SupplierBidding C WITH(nolock)
        ON A.TenderSysNo = c.TenderSysNo AND a.SupplierSysNo = c.SupplierSysNo AND c.BiddingListSysNo = a.SysNo
        INNER JOIN YZ_Supplier.dbo.Supplier D WITH(nolock)
        ON D.SysNo = A.SupplierSysNo
        INNER JOIN BidEvaluationSupplierValidity E WITH(nolock)
        ON A.SupplierSysNo = E.SupplierSysNo AND A.TenderSysNo = E.TenderSysNo
        INNER JOIN BidEvaluationSupplierPrice F ON  A.SupplierSysNo=F.SupplierSysNo AND  A.TenderSysNo=F.TenderSysNo
        WHERE a.TenderSysNo = @TenderSysNo AND ListType = 6
        AND E.OffLineBidSubmit = 1 AND E.DepositSubmit = 1
        AND C.status = 2 AND C.[Order] = 0 ORDER  BY  F.P2,F.P3
        """
    # QA DB
    msprd = connect(
        host='172.16.0.252',
        user="sa",
        password="yzw@123",
        database="YZ_Tender",
        port=14332)
    # msprd = connect(
    #     host='192.168.210.21',
    #     user="APP_Reader",
    #     password="RRI~720E$fe2gIfIrr",
    #     database="YZ_Tender",
    #     port=1433)

    # PRD DB
    # ms = MSSQL(
    #     host='192.168.210.16',
    #     user="APP_Reader",
    #     pwd="RRI~720E$fe2gIfIrr",
    #     db="YZ_Tender",
    #     port=1433)

    sql = GetBidSql.replace('@TenderSysNo', TenderSysNo)
    cursor = msprd.cursor()
    cursor.execute(sql)
    resList = cursor.fetchall()
    pro_list = []
    bidList = []
    for r in resList:
        j = json.loads(r[3])
        j = json.dumps(j, indent=4)
        j = json.loads(j)
        itemPrice = []
        for item in j["data"]:
            if int(item['id'])>=2   :   # 不要废标供应商的数据
                pro_name = item['ProductCommonName']
                pro_model = item['Model']
                itemPrice = item["sqj"]
                pro_list.append([pro_name.encode('GB2312'), itemPrice, pro_model.encode('GB2312')])
    pro_list.sort(key=lambda x: int(x[1]))
    # for item in pro_list:
    #     print item[0], "\t", item[1], "\t", item[2]
    for r in resList:
        j = json.loads(r[3])
        j = json.dumps(j, indent=4)
        j = json.loads(j)
        itemPrice = []
        for item in j["data"]:
            if int(item['id'])<=23 :
                itemPrice = itemPrice+ [float(xstr(item["sqj"])) * float(xstr(item["Quantity"]))]
        bidList.append([r[1], sum(itemPrice)])

    bidList.sort(key=lambda x: int(x[1]))
    for item in bidList:
        print (item[0], "\t", item[1], "\t" , item[2])


    return [float(price[1]) for price in bidList]




def CalBPrice(PriceList):
    # B 价只取10%~60%排名的供应商报价，排名取整数，0取1
    if int(len(PriceList) * 0.1) == 0:
        BeginIndex = 0
    else:
        BeginIndex = int(len(PriceList) * 0.1) - 1
    EndIndex = int(len(PriceList) * 0.6)
    ValidB1 = PriceList[BeginIndex:EndIndex]
    # 计算 B价
    B1Price = round(sum(ValidB1), 2) / len(ValidB1)
    print ("有效投标：",len(PriceList),"家",PriceList)
    print ("B价计算区间：: ", BeginIndex+1, "至:", EndIndex)
    print ("B价计算金额：",ValidB1)
    print ("B价：", B1Price)


if __name__ == '__main__':
    GetBid('650125')
