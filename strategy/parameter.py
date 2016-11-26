#!/usr/bin/env python
# coding:utf-8
# 
from huobi.HuobiMain import * 
import json,urllib2
import sys
import os
append_path =  os.path.dirname(os.getcwd())
sys.path.append(append_path)
import urllib2,json,time,threading
from handlers.data_collection import db as d
import requests

class parameter():
    def __init__(self):
        try:
            ticker_ltc = requests.get(r'http://api.huobi.com/staticmarket/ticker_ltc_json.js',timeout=5)
            self.ticker_ltc = ticker_ltc.json()
            ticker_ltc.close()
            #卖一价
            self.limit_price = self.ticker_ltc['ticker']['sell']
            #买一价
            self.buyone_price = float(self.ticker_ltc['ticker']['buy'])
            #交易总量 
            self.trade_total = self.ticker_ltc['ticker']['vol']
        except BaseException as e:
            self.trade_total = 0
            print u'无法获取数据',e
            return

if __name__ == '__main__':
    parameter = parameter()
    parameter.__init__()
    print parameter.buyone_price