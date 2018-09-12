# -*- coding: utf-8 -*-
__author__ = 'admin'
import pyquery as pq
import json
from file_operation import write_file

def key_err(my_dict=[], my_key=''):
    my_dict = my_dict
    my_keyword = my_key
    if my_dict.has_key(my_keyword)== True:
        result = my_dict[my_keyword]
    else:
        result = None
    return result



def contract_list():
    tender_list ="""
{"columnData":[{"headerText":"数据编号","columnType":"text","isPercent":false,"columnName":"DataSysNo","columnWidth":"100px","enableEdit":false,"enableUserType":"System","visible":false,"enableSummaryData":false,"computationRule":"","isRequired":false,"evaluationShowType":"NoDisplay","isValidate":false,"validateExp":"","_SortIndex":99},{"headerText":"数据类型","columnType":"text","isPercent":false,"columnName":"DataType","columnWidth":"100px","enableEdit":false,"enableUserType":"System","visible":false,"enableSummaryData":false,"computationRule":"","isRequired":false,"evaluationShowType":"NoDisplay","isValidate":false,"validateExp":"","_SortIndex":100},{"headerText":"劳务清单项类型","columnType":"text","isPercent":false,"columnName":"RowType","columnWidth":"100px","enableEdit":false,"enableUserType":"System","visible":false,"enableSummaryData":false,"computationRule":"","isRequired":false,"evaluationShowType":"NoDisplay","isValidate":false,"validateExp":"","_SortIndex":101},{"headerText":"商品类别","columnType":"text","isPercent":false,"columnName":"CategoryName","columnWidth":"100px","enableEdit":false,"enableUserType":"System","visible":true,"enableSummaryData":false,"computationRule":"","isRequired":false,"evaluationShowType":"Display","isValidate":false,"validateExp":"","_SortIndex":1},{"headerText":"商品名称","columnType":"text","isPercent":false,"columnName":"ProductCommonName","columnWidth":"100px","enableEdit":false,"enableUserType":"System","visible":true,"enableSummaryData":false,"computationRule":"","isRequired":false,"evaluationShowType":"Display","isValidate":false,"validateExp":"","_SortIndex":2},{"headerText":"规格型号","columnType":"text","isPercent":false,"columnName":"Model","columnWidth":"100px","enableEdit":false,"enableUserType":"System","visible":true,"enableSummaryData":false,"computationRule":"","isRequired":false,"evaluationShowType":"Display","isValidate":false,"validateExp":"","_SortIndex":3},{"headerText":"报价依据","columnType":"text","isPercent":false,"columnName":"QuotedBasis","columnWidth":"100px","enableEdit":true,"enableUserType":"Tenderer","visible":true,"enableSummaryData":false,"computationRule":"","isRequired":false,"evaluationShowType":"Display","isValidate":false,"validateExp":"","_SortIndex":4},{"headerText":"招标数量","columnType":"number","isPercent":false,"columnName":"Quantity","columnWidth":"80px","enableEdit":true,"enableUserType":"Tenderer","visible":true,"enableSummaryData":false,"computationRule":"","isRequired":true,"evaluationShowType":"Display","isValidate":false,"validateExp":"","_SortIndex":5},{"headerText":"报价","columnType":"number","isPercent":false,"columnName":"QuotedPrice","columnWidth":"80px","enableEdit":false,"enableUserType":"Bidder","visible":true,"enableSummaryData":false,"computationRule":"","isRequired":true,"evaluationShowType":"Quoted","isValidate":false,"validateExp":"","_SortIndex":6},{"headerText":"描述信息","columnType":"text","isPercent":false,"columnName":"Description","columnWidth":"100px","enableEdit":false,"enableUserType":"Bidder","visible":true,"enableSummaryData":false,"computationRule":"","isRequired":false,"evaluationShowType":"NoDisplay","isValidate":false,"validateExp":"","_SortIndex":7},{"headerText":"合价","columnType":"computation","isPercent":false,"columnName":"Valence","columnWidth":"80px","enableEdit":false,"enableUserType":"Tenderer","visible":true,"enableSummaryData":false,"computationRule":"Quantity*QuotedPrice","isRequired":false,"evaluationShowType":"NoDisplay","isValidate":false,"validateExp":"","_SortIndex":11,"computationRuleText":"招标数量*报价"},{"headerText":"单位","columnType":"text","isPercent":false,"columnName":"Unit","columnWidth":"100px","enableEdit":true,"enableUserType":"Tenderer","visible":true,"enableSummaryData":false,"computationRule":"","isRequired":false,"evaluationShowType":"Display","isValidate":false,"validateExp":"","_SortIndex":12},{"headerText":"计量单位","columnType":"text","isPercent":false,"columnName":"UnitName","columnWidth":"100px","enableEdit":true,"enableUserType":"Tenderer","visible":true,"enableSummaryData":false,"computationRule":"","isRequired":false,"evaluationShowType":"Display","isValidate":false,"validateExp":"","_SortIndex":13},{"headerText":"工作","columnType":"text","isPercent":false,"columnName":"gznr","columnWidth":"100px","enableEdit":true,"enableUserType":"Tenderer","visible":true,"enableSummaryData":false,"computationRule":"","isRequired":false,"evaluationShowType":"Display","isValidate":false,"validateExp":"","_SortIndex":14}],"data":[{"_isShow":true,"DataSysNo":"14350","DataType":"CategoryAndProduct","RowType":"category","CategoryName":"最大@12abc;de 最大@12abc;de 最大@12abc;de 最大@完","ProductCommonName":"","Model":"","QuotedBasis":"","Quantity":"23.1","QuotedPrice":null,"Description":"","Valence":"","Unit":"12","UnitName":"","gznr":"","id":1},{"_isShow":true,"DataSysNo":"100001363","DataType":"ProductCommon","RowType":"item","CategoryName":"最大@12abc;de 最大@12abc;de 最大@12abc;de 最大@完","ProductCommonName":"最大@12abc;de 最大@12abc;de 最大@12abc;de 最大@完","Model":"","QuotedBasis":"","Quantity":"21.11","QuotedPrice":null,"Description":"","Valence":"","Unit":"立方米","UnitName":"立方米","gznr":"","id":2},{"_isShow":true,"DataSysNo":"598858","DataType":"ProductCommon","RowType":"item","CategoryName":"最大@12abc;de 最大@12abc;de 最大@12abc;de 最大@完","ProductCommonName":"最大@12abc;de 最大@12abc;de 最大@12abc;de 最大@完","Model":"","QuotedBasis":"","Quantity":"1221.11","QuotedPrice":null,"Description":"","Valence":"","Unit":"1211","UnitName":"1211","gznr":"","id":3},{"_isShow":true,"DataSysNo":"3139","DataType":"CategoryAndProduct","RowType":"category","CategoryName":"综合用工","ProductCommonName":"","Model":"","QuotedBasis":"","Quantity":"233.1","QuotedPrice":null,"Description":"","Valence":"","Unit":"12","UnitName":"12","gznr":"","id":4},{"_isShow":true,"DataSysNo":"100001662","DataType":"ProductCommon","RowType":"item","CategoryName":"综合用工","ProductCommonName":"综合用工","Model":"","QuotedBasis":"","Quantity":"231","QuotedPrice":null,"Description":"","Valence":"","Unit":"件","UnitName":"件","gznr":"","id":5},{"_isShow":true,"DataSysNo":"100001425","DataType":"ProductCommon","RowType":"item","CategoryName":"综合用工","ProductCommonName":"综合用工","Model":"","QuotedBasis":"","Quantity":"123","QuotedPrice":null,"Description":"","Valence":"","Unit":"立方米","UnitName":"立方米","gznr":"","id":6}],"NC_DataType":0,"NC_DataSysNo":34032}
"""
    my_list = json.loads(tender_list)['data']
    coloum_list = list()
    for item in my_list:
        DataSysNo = int(key_err(item, 'DataSysNo'))
        DataType = key_err(item, 'DataType')
        DataCateName = key_err(item, 'CategoryName')
        QuotedBasis = key_err(item, 'QuotedBasis')
        Model = key_err(item, 'Model')
        ForeignCode = None
        Character = None
        QuotedBasis = key_err(item, 'QuotedBasis')
        JobContent = key_err(item, 'gznr')
        Remark = key_err(item, 'Description')
        if item.has_key('UnitName') == True:
            UnitName = item['UnitName']
        else:
            UnitName = key_err(item, 'Unit')

        TotalPrice = key_err(item, 'hj')
        if key_err(item, 'RowType')=='category':
            RowType=0
        else:
            RowType=1

        if DataType=='CategoryAndProduct' or DataType == 'Category':
            Quantity = key_err(item, 'Quantity')
            DataName = key_err(item, 'CategoryName')
            UnitPrice = key_err(item, 'QuotedPrice')
        elif DataType == "ProductCommon" or DataType == "Product":
            Quantity = key_err(item, 'Quantity')
            DataName = item['ProductCommonName']
            UnitPrice = key_err(item, 'QuotedPrice')

        else:
            DataName = key_err(item, 'Name')
            Quantity = key_err(item, 'GCL')
            ForeignCode = key_err(item, 'ForeignCode')
            Character = key_err(item, 'Character')
            UnitPrice = key_err(item, 'ComUnitPrice')

        coloum_list.append((DataSysNo, DataType, RowType, Quantity, DataName, DataCateName, QuotedBasis,
                            Model, ForeignCode, Character, UnitName, JobContent, Remark, UnitPrice, TotalPrice,))
    coloum_list.sort()
    coloum_list = coloum_list
    return coloum_list




if __name__ == '__main__':
    my_list = contract_list()
    write_file('122121', my_list)