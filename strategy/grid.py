#!/usr/bin/env python
# coding:utf-8
# 
import sys
import os
append_path =  os.path.dirname(os.getcwd())
sys.path.append(append_path)
import urllib2,json,time,threading
from handlers.data_collection import db as d
from personalHandler import personalHandler as p 
import general

__author__ = 'KlausQiu'

#日期时间，开盘价，最高价，最低价，收盘价，成交量
class fibonacci:
    def __init__(self,uid):
        try:
            self.ticker_ltc = json.loads(urllib2.urlopen(r'http://api.huobi.com/staticmarket/ticker_ltc_json.js').read())
            self.kline_datas = json.loads(urllib2.urlopen(r'http://api.huobi.com/staticmarket/ltc_kline_100_json.js').read())
            #目前是看最近30天内的最高和最低
            self.highPirce =max([self.kline_datas[n][2] for n in range(-30,0)])
            self.lowPirce = min([self.kline_datas[n][3] for n in range(-30,0)])
            #斐波那契的黄金分割系数
            self.coefficient = [1,0.786,0.618,0.5,0.382,0.236]
            #算出各个点的价格，建立区间
            self.fibonacci_interval = map(general.float_format,self.handlerPrice())
            #把系数和价格区间对应起来
            self.relation = dict(zip(self.coefficient,self.fibonacci_interval))
            #买入比例（按总金额）
            self.buyProportion = {0.618:0.6,0.5:0.4,0.382:0.7,0.236:1}
            #卖出比例(按持有币数)
            self.sellProportion = {1:0.1,0.786:0.3,0.618:0.6,0.5:0.31,0.382:0.4,0.236:0.7}
            #用户自定义仓位
            self.uid = uid
            self.freightSpace = self.freightSpace()
            self.fibonacciResult = self.FResult()
        except BaseException as e:
            print '暂时无法获取数据',e


    def handlerPrice(self):

        fibonacci_price = self.highPirce-self.lowPirce
        fibonacci_interval = []
        for c in self.coefficient:
            fibonacci_interval.append(self.lowPirce+c*fibonacci_price)
        fibonacci_interval.append(self.lowPirce)
        return fibonacci_interval

    def freightSpace(self):
        db = d.db_control()
        result = db.select('user',uid = self.uid)
        self.fibonacciGrid = ((db.select('fibonacciGrid',UID=self.uid))[0][2]).split(",")
        personal = p(result[0][4], result[0][5])
        freightSpace = personal.freightSpace
        return freightSpace

    def FResult(self):
        fibonacci = []
        names = ['一区(空)','二区(RUN)','三区(X)','四区(RUN)','五区(多)','六区(多)']
        self.nowInterval = self.now_interval()
        for n in range(0,6):
            fibonacci.append({"name":names[n],"position":self.fibonacciGrid[n],"today":self.fibonacci_interval[n],"yesterday":self.fibonacci_interval[n+1]})
            if fibonacci[n]["today"] == self.nowInterval[0]:
                fibonacci[n]["freightSpace"] = self.freightSpace
        result = fibonacci
        return result

    def now_interval(self):
        f = self.fibonacci_interval
        print f
        self.buyone_price = self.ticker_ltc['ticker']['buy']
        now_interval = []
        print self.buyone_price
        for n in f:
            if n >= self.buyone_price >= f[f.index(n)+1]:
                print n,f[f.index(n)+1]
                now_interval = map(general.float_format,[f[f.index(n)],f[f.index(n)+1]])
                return now_interval


