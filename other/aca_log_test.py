__author__ = 'Administrator'
import threading
import time
import raven


# 高校日志测试
def wrtie_log():
    client = raven.Client(dsn='http://1c4c44b462424b9791c926ce5c09cea6:4573104983b945a19ff1167241d4896c@182.140.231.146:9000/2')
    for i in  range(100):
        client.captureMessage('hell test')
        print 'ok'
        time.sleep(1)

ts = [threading.Thread(target=wrtie_log, name='threading0') for i in range(10)]
for t in ts:
    t.start()
    t.join()
