# -*- coding: utf-8 -*-
__author__ = 'admin'
import requests

def crash_lps3():
    s = requests.session()
    # header = {"Accept": "application/json, text/javascript, */*; q=0.01",
    #           "Accept-Encoding": "gzip, deflate",
    #           "Accept-Languag": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    #           "Connection": "keep-alive",
    #           "Content-Length": "56",
    #           "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    #           "Cookie": "CNZZDATA1259625247=679227347-1476409933-http%253A%252F%252Fauth.yzw.cn.qa%253A8000%252F%7C1476421248; Hm_lvt_5319ed054e5397c684cb53f8f589586e=1479903674,1479955833,1479989887,1480042073; Hm_lpvt_5319ed054e5397c684cb53f8f589586e=1480042079; auth.verifycode.yzw=8B47C2CFDE0C38C578A95EE4CEDADAAD38616B9E2C5812B7892D34",
    #           "HOST": "auth.yzw.cn.qa:8000",
    #           "Referer": "http://auth.yzw.cn.qa:8000/Login/V2",
    #           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    #           "X-Requested-With	": "XMLHttpRequest",
    #
    #           }
    # form_data = {'account': 'jcadmin', 'keepalive': 'false', 'password': '111111', 'verifycode': '1000'}
    # # post 换成登录的地址，
    # s.post('http://auth.yzw.cn.qa:8000/Login/V2', data=form_data, headers=header)
    # # 换成抓取的地址
    # f = s.get('http://portal.jc.yzw.cn.qa:8000/')
    # print 'test'
    from_data = {"SysNo":"","ContractDocumentCode":"","ContractName":"","TenderName":"","SupplierName":"","ProjectName":"","OrganizationCode":"","ContractType":"","InUserName":"","Status":"","SignDateFrom":"","SignDateTo":"","InDateFrom":"","InDateTo":"","IsQuerySubContract":False,"SystemCategoryTypeList":[]}
    s = requests.post('https://jc.yzw.cn/ContractMgt/Contract/Query', data=from_data, cookies={'web.auth.yzw':'7046507680830CEF48254401C1D8E1147124E1CAF325FA3FB93D615753B362A27A6C1F2712AAE534BA95C9F59A3EC38FE85B9A8FBDDDD9B0415257C395590AAC97BFE0177626172AF65AD4C65B05297C70ACAB345C29B021EB1E692AB4898F81A251E8391BACE478A4230C2E8F2F1F9245E7350BF768AE0593636027D9D629159A9C58D7385FA7E32B6DFF2418E411D920A3C58532C30BF769E8E3BF6AA9B60C14C70EEFE2179D1D33B940B0CA5E7669DCAE6C479E279BBE8DFBA533CC3C27E9C1BF46769FF09931D58B10624D43F5862D7280C4BE0FB5E374784A2AE8007538A80A89A63F934A392E5D6556988D535134F6559609CE049A6592AC1313EACBABCECF6B7958873E49B21030FB9BDE2D8D893638A820BF3954A83116A069A23CB52D7E42D142C1E3DC1CCCE972B51205DF4B4A14EEE109DF38D346DF626227886387FE3C40FD764E3DB824A3DC9509947E1A107A999D33A705F40B50CDDFB4470086452E8D6F7755FDFE27FF92D3194D7526DBCD3794E0FEEA3B5E7807C734C6E0B26D02E27B7142ADBBFB7D2459B59F809048DCDA674E6117058E88837C303D89FD7E3889D906103891931FC0AD607A3BA22526E5D54BD13D05B9B4DDD9802486D482FF01B5F6E920205652549E0F951236D24F32973094EC3897CF20A902F7FBBDEFCAE11BB61DB907AA78D797414BA696C9D798820F5D0BCAD5EA76AB58F2554E6C2AAC11AF2521A5DD52E198820878177028F1C50AF4326C74DB1B3628CEFB54FCE7959B4BC2630523EE4188F6F98C42F63207FE77CF25'})
    print s
    print 'test'

if __name__ == '__main__':
    crash_lps3()