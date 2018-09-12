__author__ = 'Administrator'
import urllib2
import requests
import time
from mysql import conn
# def check(website):
#     try:
#         response = urllib2.urlopen(website)
#         html = response.read()
#         print(html)
#     except urllib2.URLError as e:
#         result = e
#     return result

connect = conn.cursor()
connect.execute('SELECT url FROM urls WHERE  result IS NULL ')
List = connect.fetchall()

for i in range(4000):
    value1 = List[i][0]
    test = requests.get('http://www.maiziedu.com/uploads/'+List[i][0])
    staus = test.status_code
    connect.execute('update urls SET result="{staus}" WHERE url="{value1}"'.format(staus=staus, value1=value1))
    conn.commit()
    time.sleep(1)




# check('http://www.maiziedu.com/uploads/avatar/2015/05/ce30786e-010f-11e5-aeef-00163e02100b_middle.jpg/')

