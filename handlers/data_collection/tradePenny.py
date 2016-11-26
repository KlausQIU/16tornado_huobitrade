import sys
import os
from huobi.Util import *
from huobi import HuobiService
import urllib2,json,time,threading
from datetime import datetime
import requests

__author__ = 'KlausQiu'

class tradePenny():
    def __init__(self,uid):
        try:
            ticker_ltc = requests.get(r'http://api.huobi.com/staticmarket/ticker_ltc_json.js',timeout=5)
            self.ticker_ltc = json.loads(ticker_ltc.text)
            ticker_ltc.close()
            self.account_info = HuobiService.getAccountInfo(ACCOUNT_INFO)
            self.getOrder = HuobiService.getOrders(2,GET_ORDERS)
            #卖单数量
            self.sellOne_count = [order for order in self.getOrder if order['type'] == 2]
            #买单数量
            self.buyOne_count = [order for order in self.getOrder if order['type'] == 1]
            #已完成的委托
            self.dealOrders =  HuobiService.getNewDealOrders(2,NEW_DEAL_ORDERS)
            #资产折合
            self.total = float(self.account_info['total'])
            #卖一价
            self.limit_price = self.ticker_ltc['ticker']['sell']
            #买一价
            self.buyone_price = self.ticker_ltc['ticker']['buy']
            #总量
            self.trade_total = self.ticker_ltc['ticker']['vol']
            #限制挂单数量
            self.orderCount = self.handler_orderCount()
            #可用资金
            self.a_cny_display = float(self.account_info['available_cny_display'])
            #可用莱特币
            self.a_ltc_display = float(self.account_info['available_ltc_display'])
        except BaseException as e:
            print u'无法获取数据',e