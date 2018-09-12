# -*- coding: utf-8 -*-
__author__ = 'admin'
from pymssql import connect

def test_conn():
    sql_conn = connect(host='172.16.0.252', user='sa', password='yzw@123', database='YZ_Tender', port=14332)
    # sql_conn = connect(host='172.16.0.252:14332\TENDER', user='sa', password='yzw@123', database ="YZ_Tender")
    return sql_conn

def select(sql):
    conn = test_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
    except Exception:
        res = u'语句有问题'
    cursor.close()
    conn.close()
    return res
TenderSysNo = 20274
sign_up_sql = """
SELECT TOP(1000) SupplierSysNo FROM  TenderSupplier with(nolock)  WHERE status =30 AND  TenderSysNo  = {TenderSysNo};
"""
tender_sql = """
SELECT TOP(1000) SupplierSysNo FROM  TenderSupplier with(nolock)  WHERE  status IN (60,70,80,90)AND   TenderSysNo  = {TenderSysNo};
"""


if __name__ == "__main__":
    print u'李朗', select(sign_up_sql)
    print 'test'
