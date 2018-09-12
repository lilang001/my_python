
# -*- coding: utf-8 -*-
__author__ = 'Administrator'



import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# def fps_con():
#
#     try:
#
#         conn =MySQLdb.connect(host='192.168.1.142', user='root', passwd='1234', db='fps_20151217', port=3306,charset='utf8')
#         conn = fps_conn()
#         cur=conn.cursor()
#         cur.execute('select *  from mz_forum_entity where user=2218 order BY date_publish  DESC limit 0,1 ')
#         # cur.execute("select * from mz_forum_entity limit 0 , 1")
#
#         for row in cur:
#             print (row["content"])
#
#         if row["content"]=='<p>content is hell hello world</p>':
#             print('pass')
#         else:print('failed')
#         cur.close()
#         conn.close()
#     except Exception as e:
#         print(e)



# 更新自动化数据库方法
def auto(sql):
    conn = auto_conn()
    output_cursor = conn.cursor()
    try:

        res = output_cursor.execute(sql)
        conn.commit()
    except Exception:
        pass
    output_cursor.close()
    conn.close()
    return res

# db_lps = 'lps_lilang'
# db_fps = 'fps_20151217'

# 查询数据库方法
def select(sql):
    conn = maizi_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
    except Exception as e:
        print(e)
        res = u'语句有问题'
    cursor.close()
    conn.close()
    return res


# 拼接数据库查询sql
def data(database, table_name, args, **kwargs):
    sel = ''
    for arg in args:
        sel += arg + ','
    sel = sel[:-1]
    where_sql = ''
    for key in kwargs.keys():
        where_sql += key + '="' + str(kwargs[key]) + '" and '
    where_sql = where_sql[:-4]
    print(where_sql)
    sql = """SELECT {sel} FROM {database}.{table_name} WHERE  {where_sql};"""
    res = select(sql.format(sel=sel, where_sql=where_sql, table_name=table_name, database=database))
    return res


# 定义自动化测试库的sql链接
def auto_conn():
    sql_conn = MySQLdb.connect(host='192.168.1.142', user='root', passwd='1234', db='AutoTesting', port=3306, charset='utf8')
    return sql_conn


# 定义麦子业务数据库sql链接
def maizi_conn():
    sql_conn = MySQLdb.Connect(host='192.168.1.142', user='root', passwd='1234', db='fps_20151217', port=3306, charset='utf8')
    return sql_conn


# 更新自动化测试库数据,更新期望结果,实际结果,执行结果
def update_output(method, expect, actual):
    output_sql = """
    update TestCase SET expect_output="{expect}",actual_output="{actual}",test_result="{result}" WHERE method="{method}";
    """
    if expect == actual and expect is not None:
        result = "通过"
    else:
        result = "不通过"
    auto(output_sql.format(expect=expect, actual=actual, result=result, method=method))




