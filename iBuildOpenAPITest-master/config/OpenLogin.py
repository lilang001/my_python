#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

QA = {"Host": "http://172.16.0.132:81"}


class supplierInfo():
    def __init__(self, user, passwd, ENV):
        """
        模拟供应商登陆，获取session，供后续请求使用
        """
        self.Host = ENV['Host']
        self.se = requests.Session()
        self.se.post(
            self.Host + "/api/auth/login/",
            json={
                "loginName": user,
                "password": passwd,
                "captcha": "",
                "captchaToken": 1531723663368,
                "remberMe": False
            })

    def getInfo(self):
        """
        获取供应商详情：「accessID」「accessKey」
        """
        res = self.se.get(self.Host + "/api/open/supplier/displaySettings")
        return res.json()

    def getDeviceList(self, ProjectSysNo=''):
        """
        不传项目编号：返回所有激活的设备
        传项目编号：返回该供应商指定项目激活的设备
        """
        SoftwareList = self.se.post(
            self.Host + "/api/open/product/pageList",
            json={"pageNum": 1,
                  "pageSize": 100,
                  "type": 1})
        DeviceList = []
        for sw in SoftwareList.json()['data']['list']:
            DevList = self.se.post(
                self.Host + "/api/open/productDevice/list",
                json={
                    "pageNum": 1,
                    "pageSize": 100,
                    "productSysNo": sw['sysNo']
                })
            # print(json.dumps(DevList.json(), indent=2, ensure_ascii=False))
            if DevList.json()['data']['list']:
                tmpProduct = {}
                tmpProduct['productName'] = sw['productName']
                tmpProduct['DeviceList'] = []
                for prj in DevList.json()['data']['list']:
                    prj['catalogCode'] = sw['catalogCode']
                    prj['catalogName'] = sw['catalogName']
                    if prj['activateStatus'] == 1:
                        if ProjectSysNo == '':
                            tmpProduct['DeviceList'].append(prj)
                        elif ProjectSysNo == prj['projectSysNo']:
                            tmpProduct['DeviceList'].append(prj)
                DeviceList.append(tmpProduct)
        return DeviceList

    def getSoftwareProjects(self, ProjectSysNo=''):
        """
        不传项目编号：返回所有软件产品的所有项目
        传项目编号：返回所有软件产品，指定的项目
        """
        SoftwareList = self.se.post(
            self.Host + "/api/open/product/pageList",
            json={"pageNum": 1,
                  "pageSize": 100,
                  "type": 2})
        Projects = []
        for sw in SoftwareList.json()['data']['list']:
            ProjectList = self.se.post(
                self.Host + "/api/open/product/listProject",
                json={
                    "pageNum": 1,
                    "pageSize": 10,
                    "sysNo": sw['sysNo'],
                    "type": 2
                })
            if len(ProjectList.json()['data']['list']) > 0:
                tmpProduct = {}
                tmpProduct['productName'] = sw['productName']
                tmpProduct['ProjectList'] = []
                for prj in ProjectList.json()['data']['list']:
                    prj['catalogCode'] = sw['catalogCode']
                    prj['catalogName'] = sw['catalogName']
                    prj['productName'] = sw['productName']
                    if ProjectSysNo == '':
                        tmpProduct['ProjectList'].append(prj)
                    elif prj['projectSysNo'] == ProjectSysNo:
                        tmpProduct['ProjectList'].append(prj)
                Projects.append(tmpProduct)
        return Projects


if __name__ == "__main__":
    se = supplierInfo('sup120', '111111', QA)

    res = se.getInfo()
    print(json.dumps(res, indent=4, ensure_ascii=False))
    print("\n")

    res = se.getDeviceList()
    print(json.dumps(res, indent=4, ensure_ascii=False))
    print("\n")

    res = se.getSoftwareProjects(10218)
    print(json.dumps(res, indent=4, ensure_ascii=False))
    print("\n")
