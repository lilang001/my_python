#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os, json
DIR_PATH = os.path.dirname(os.path.abspath(__file__ + "/../"))
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# print("sub: ", DIR_PATH)


def logSuccess(ENV, filename, status, url, request, response):
    LogFileName = datetime.datetime.now().strftime(
        "%Y%m%d") + filename + '.log'
    with open(
            DIR_PATH + '/log/' + ENV + '/' + LogFileName, 'a+',
            encoding="utf-8") as data_file:
        data_file.write("\n========================Log Begin====")
        data_file.write("\nStatus: " + status)
        data_file.write("\nDate: " + datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"))
        data_file.write("\nUrl: " + url)
        data_file.write("\nRequest: ")
        data_file.write("\n" + request)
        data_file.write("\nResponse: ")
        data_file.write("\n")
        data_file.write(str(response))
        data_file.write("\n========================Log End====")
        data_file.write("\n")
        data_file.close()


def logError(ENV, filename, status, url, request, response):
    LogFileName = datetime.datetime.now().strftime(
        "%Y%m%d") + filename + '_Error.log'
    with open(
            DIR_PATH + '/log/' + ENV + '/' + LogFileName, 'a+',
            encoding="utf-8") as data_file:
        data_file.write("\n========================Log Begin====")
        data_file.write("\nStatus: " + status)
        data_file.write("\nDate: " + datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"))
        data_file.write("\nUrl: " + url)
        data_file.write("\nRequest: ")
        data_file.write("\n" + request)
        data_file.write("\nResponse: ")
        data_file.write("\n")
        data_file.write(str(response))
        data_file.write("\n========================Log End====")
        data_file.write("\n")
        data_file.close()


def logSmoke_detector(ENV, ProjectSysNo, WarningID):
    filename = DIR_PATH + '/log/' + ENV + '/smoke_detector.json'
    ProjectSysNo = str(ProjectSysNo)
    tmp = {ProjectSysNo: []}
    a = json.load(open(filename, encoding="utf-8"))
    if os.path.isfile(filename, encoding="utf-8"):
        d = json.load(open(filename, encoding="utf-8"))

        if ProjectSysNo in d.keys():
            if WarningID in d[ProjectSysNo]:
                d[ProjectSysNo].remove(WarningID)
            else:
                d[ProjectSysNo].append(WarningID)
        else:
            d[ProjectSysNo] = []
            d[ProjectSysNo].append(WarningID)

        with open(filename, "w", encoding="utf-8") as data:
            data.write(json.dumps(d, indent=4))
            data.close()
    else:
        with open(filename, 'a+', encoding="utf-8") as data:
            tmp[ProjectSysNo].append(WarningID)
            data.write(json.dumps(a, indent=4))
            data.close()
        return []


def getSmoke_detector(ENV, ProjectSysNo):
    filename = DIR_PATH + '/log/' + ENV + '/smoke_detector.json'
    ProjectSysNo = str(ProjectSysNo)
    a = {ProjectSysNo: []}
    if os.path.isfile(filename):
        with open(filename, encoding="utf-8") as data:
            a = data.read()
            d = json.loads(a)
            data.close()
            if ProjectSysNo in d:
                return d[ProjectSysNo]
            else:
                return []
    else:
        with open(filename, 'a+', encoding="utf-8") as data:
            data.write(json.dumps(a, indent=4))
            data.close()
        return []


def log_vehicleNumber(ENV, ProjectSysNo, vehicleNumber, entryOrExit,
                      regiteredVehicle):
    ProjectSysNo = str(ProjectSysNo)
    filename = DIR_PATH + '/log/' + ENV + '/' + ProjectSysNo + 'vehicleNumber.json'

    if os.path.isfile(filename):
        tmp = json.load(open(filename, encoding="utf-8"))
    else:
        tmp = {}

    tmp[vehicleNumber] = {
        "entryOrExit": entryOrExit,
        "regiteredVehicle": regiteredVehicle
    }
    with open(filename, "w", encoding="utf-8") as data:
        # data.write(json.dumps(tmp, indent=4,ensure_ascii = False).encode('utf-8'))
        data.write(json.dumps(tmp, indent=4, ensure_ascii=False))
        data.close()

        # return []


def get_vehicleNumber(ENV, ProjectSysNo, vehicleNumber):
    ProjectSysNo = str(ProjectSysNo)
    filename = DIR_PATH + '/log/' + ENV + '/' + ProjectSysNo + 'vehicleNumber.json'

    if os.path.isfile(filename):
        with open(filename, encoding="utf-8") as data:
            tmp = json.load(data)

            if vehicleNumber in tmp.keys():
                return tmp[vehicleNumber]
            else:
                return {}
            data.close()
    else:
        return {}


if __name__ == "__main__":

    # a = getSmoke_detector("QA", "10002")
    # logSmoke_detector("QA","10002",{
    #         "ID": "b2dc5e5f-9921-49a7-bb8d-e683b73f2ef3",
    #         "event_type": "03"
    #     })
    # a = getSmoke_detector("QA", "10002")
    # print(a)
    name = "川A3331"
    # c=unicode(name,'utf-8')
    # a=log_vehicleNumber("QA", "10078",c,1,False)
    a = get_vehicleNumber("QA", "10079", name)
    print(a)
# print(a)
