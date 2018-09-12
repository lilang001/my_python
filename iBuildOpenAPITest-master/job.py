#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import time
from config.AppConfig import ENV as OpenAPIEnv
from config.OpenLogin import supplierInfo
import OpenAPI
import importlib
from config.cataLogConfig import catalogMethodMap

dir_path = os.path.dirname(os.path.realpath(__file__))


class GenerateDataJob():
    def __init__(self):
        self.Env = OpenAPIEnv
        self.supplier = supplierInfo(
            user=OpenAPIEnv['user'],
            passwd=OpenAPIEnv['passwd'],
            ENV=OpenAPIEnv)

    def getAccessIDKey(self):
        res = self.supplier.getInfo()
        self.Env['Code'] = res['data']['accessID']
        self.Env['Key'] = res['data']['accessKey']
        return res['data']['accessID'], res['data']['accessKey']

    def sendOpenAPI(self, req, method):
        res = OpenAPI.OpenAPI(
            p_appid=self.Env['Code'],
            p_appsecret=self.Env['Key'],
            method=method,
            data=json.dumps(req))
        print(res.json())
        if res.json()['code'] != 0:
            print("Send OpenAPI Fail")

    def runDevice(self):
        devices = self.supplier.getDeviceList()
        for catalog in devices:
            if len(catalog['DeviceList']) > 0:
                app = importlib.import_module(
                    'apps.' + catalog['DeviceList'][0]['catalogCode'],
                    package=__package__)
                for m in catalogMethodMap:
                    if m['cataLogCode'] == catalog['DeviceList'][0][
                            'catalogCode']:
                        method = m['method']
                for d in catalog['DeviceList']:
                    res = app.JSONV2_Request(d['deviceCode'])
                    self.sendOpenAPI(res, method)
                    # print(json.dumps(res, indent=2, ensure_ascii=False))
                # print(json.dumps(devices, indent=2, ensure_ascii=False))

    def runSoftWear(self):
        SProjects = self.supplier.getSoftwareProjects()
        # print(json.dumps(SProjects, indent=2, ensure_ascii=False))
        for project in SProjects:
            if len(project['ProjectList']) > 0:
                app = importlib.import_module(
                    'apps.' + project['ProjectList'][0]['catalogCode'],
                    package=__package__)
                for m in catalogMethodMap:
                    if m['cataLogCode'] == project['ProjectList'][0][
                            'catalogCode']:
                        method = m['method']
                for p in project['ProjectList']:
                    res = app.JSONV2_Request(p['projectSysNo'])
                    self.sendOpenAPI(res, method)


if __name__ == "__main__":
    G = GenerateDataJob()

    while True:
        G.runSoftWear()
        G.runDevice()
        time.sleep(60)
