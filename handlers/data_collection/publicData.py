#!/usr/bin/env python
# coding:utf-8

import tornado.web
import db
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from strategy import parameter as p
from strategy.setting import total_money
import requests
import json
import time
import sqlite3

__author__ = 'klausQiu'

def main():

    print 'enter PublicData collection'
    dbLink = db.db_control()
    try:
        publicData = dbLink.select('publicData')
        ltc = requests.get(r'http://api.huobi.com/staticmarket/ticker_ltc_json.js',timeout=5)
        ticker_ltc = ltc.json()['ticker']['last']
        ltcTradeVol = ltc.json()['ticker']['vol']
        btc = requests.get(r'http://api.huobi.com/staticmarket/ticker_btc_json.js',timeout=5)
        ticker_btc = btc.json()['ticker']['last']
        dealltcData = requests.get(r'http://api.huobi.com/staticmarket/detail_ltc_json.js',timeout=5)
        dealdata = dealltcData.json()
        dealdata = encode_publicData(str(dealdata['trades'][0]))
        dbLink.insert('publicData',time.strftime('%Y%m%d%H%M%S',time.localtime()),dealdata,ticker_ltc,ticker_btc,ltcTradeVol)
        count = len(dbLink.select('publicData')) if publicData else 0
        if count >= 5:
            dbLink.delete('publicData',Time=(min(dbLink.select('publicData')))[0])
        ltcData = requests.get(r'http://api.huobi.com/staticmarket/ltc_kline_015_json.js',timeout=5) 
        handlerltc = json.loads(ltcData.text)
        handlerltc = handlerltc[-200:]
        xBxisData = []
        ltcData = []
        for ltc in handlerltc:
            timeData = ltc[0][8:12]
            timeData = timeData[0:2]+':'+timeData[2:]
            xBxisData.append(timeData)
            ltc = ltc[1:5]
            h = ltc[1];
            l = ltc[2];
            c = ltc[3];
            ltc[1] = c;
            ltc[2] = l;
            ltc[3] = h;
            ltcData.append(ltc)
        dbLink.insert('ltcData',time.strftime('%Y%m%d%H%M%S',time.localtime()),encode_publicData(str(xBxisData)),ltcData)
        count = len(dbLink.select('ltcData')) if ltcData else 0
        if count >= 3:
            dbLink.delete('ltcData',Time=(min(dbLink.select('ltcData')))[0])
    except BaseException as e:
        print u'publicData colleciton fxcking the bolt shit wrong',e


def ltcData():
    print u'enter ltcData Collection'
    dbLink = db.db_control()
    try:
        ltcData = requests.get(r'http://api.huobi.com/staticmarket/ltc_kline_015_json.js',timeout=5) 
        handlerltc = json.loads(ltcData.text)
        handlerltc = handlerltc[-200:]
        xBxisData = []
        ltcData = []
        for ltc in handlerltc:
            timeData = ltc[0][8:12]
            timeData = timeData[0:2]+':'+timeData[2:]
            xBxisData.append(timeData)
            ltc = ltc[1:5]
            h = ltc[1];
            l = ltc[2];
            c = ltc[3];
            ltc[1] = c;
            ltc[2] = l;
            ltc[3] = h;
            ltcData.append(ltc)
        dbLink.insert('ltcData',time.strftime('%Y%m%d%H%M%S',time.localtime()),encode_publicData(str(xBxisData)),ltcData)
    except BaseException as e:
        print u'network wrong',e
        return 
    count = len(dbLink.select('ltcData')) if ltcData else 0
    if count >= 3:
        dbLink.delete('ltcData',Time=(min(dbLink.select('ltcData')))[0])

def encode_publicData(data):
    if isinstance(data,str):
        import re
        strinfo = re.compile("'")
        data = strinfo.sub('R1-1',data)
        return data
    else:
        print 'give me string.'

def decode_publicData(data):
    if isinstance(data,str):
        import re
        strinfo = re.compile('R1-1')
        data = strinfo.sub("'",data)
        return data
    else:
        print 'give me string.'

def publicDataReturn():
    #返回dealData，tickerltc，tickerbtc
    dbLink = db.db_control()
    publicData = dbLink.select('publicData')
    if publicData:
        data = {'time':publicData[-1][0],
                'dealdata':decode_publicData(str(publicData[-1][1])),
                'ticker_ltc':publicData[-1][2],
                'ticker_btc':publicData[-1][3],
                'ltcTradeVol':publicData[-1][4]}
        return data


def ltcDataReturn():
    dbLink = db.db_control()
    ltcData = dbLink.select('ltcData')
    if ltcData:
        data = {'xBxisData':decode_publicData(str(ltcData[-1][1])),
        'ltcData':ltcData[-1][2]
        }
    return data

if __name__ == '__main__':
    while True:
        main()
        ltcData()
        time.sleep(2)

#         enter ProfitDataColleciton
# {'dealdata':"{u'amount': 0.01, u'en_type': u'bid', u'type': u'\\u4e70\\u5165', u'price': 26.2, u'time': u'16:35:14'}",'ticker_btc':u'{"time":"1478507721","ticker":{"symbol":"btccny","vol":1426057.1482,"high":4831,"last":4792.39,"low":4713.2,"sell":4792.67,"buy":4792.39,"open":4740.9} }', 'ticker_ltc': u'{"time":"1478507721","ticker":{"symbol":"ltccny","vol":14281769.149,"high":26.39,"last":26.2,"low":26.04,"sell":26.2,"buy":26.19,"open":26.13} }'}
# Error: near "dealdata": syntax error