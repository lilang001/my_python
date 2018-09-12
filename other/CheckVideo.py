__author__ = 'Administrator'
import urllib2
import requests
import time
import threading
from mysql import conn


# 检查七牛云全站视频是否可访问
def check_video():
    connect = conn.cursor()
    connect.execute('SELECT url FROM urls WHERE  result IS NULL ')
    List = connect.fetchall()
    for i in range(4000):
        value1 = List[i][0]
        try:
            test = requests.get(value1, stream=True)
        except Exception as e:
            print e
        staus = test.status_code
        connect.execute('update urls SET result="{staus}" WHERE url="{value1}"'.format(staus=staus, value1=value1))
        conn.commit()
        time.sleep(1)
        print('test')

ts = [threading.Thread(target=check_video, name='threading1') for i in range(100)]
for t in ts:
    t.start()
    t.join()



