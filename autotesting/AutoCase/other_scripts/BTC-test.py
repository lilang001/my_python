# coding=utf-8
"""
@version: 2018/3/12
@author:
@contact:
@file:
@time: 14:35
@note:  ??
"""
from __future__ import unicode_literals

import time
import datetime
import json
import requests

url = "https://www.bit-z.com/index/infofresh?t=0.226269764221956"
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def get_latest_order(ot):
    data = requests.get(
        'https://www.bit-z.com/json/%s_order?t=0.226269764221956' % ot,
        timeout=2,
    ).json().get('d')
    t, n, p = data[0]['t'], data[0]['n'], data[0]['p']
    t = datetime.datetime.strptime(datetime.date.today().isoformat() + ' ' + t, '%Y-%m-%d %H:%M:%S')
    return (datetime.datetime.now() - t).seconds, n


get_latest_order('pok_btc')


def do():
    time.sleep(3)
    data = requests.get(url, headers=headers, timeout=2).json().get('data')
    pok_btc = json.loads(data['pok_btc'])['now_price']
    pok_btc_cny = json.loads(data['pok_btc'])['cny']
    pok_eth = json.loads(data['pok_eth'])['now_price']
    pok_eth_cny = json.loads(data['pok_eth'])['cny']
    eth_btc = json.loads(data['eth_btc'])['now_price']
    sub = (float(pok_eth) * float(eth_btc) / float(pok_btc) - 1) * 100
    pok_btc_t, pok_btc_n = get_latest_order('pok_btc')
    pok_eth_t, pok_eth_n = get_latest_order('pok_eth')
    print "pok_btc[%ss,%s]:%s(%s) %s pok_eth[%ss,%s]:%s(%s),eth_btc:%s" % (
        pok_btc_t, pok_btc_n.split('.')[0],
        pok_btc, pok_btc_cny,
        "<" if sub > 0 else '>',
        pok_eth_t, pok_eth_n.split('.')[0],
        pok_eth, pok_eth_cny, eth_btc),
    print '====%s====' % round(abs(sub), 2), '!!!!!!' if abs(sub) > 1 else ''


while 1:
    try:
        do()
    except Exception, e:
        print e
        pass

