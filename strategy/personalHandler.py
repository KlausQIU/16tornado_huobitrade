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
from strategy.huobi import HuobiService
import operator
from strategy import parameter as pa
from strategy.general import float_format as float_format

__author__ = 'KlausQiu'

def openDB(func):
    def wrap(self,*args,**kw):
        db = d.db_control()
        return func(self,db,*args,**kw)
    return wrap

class personalHandler():
    """docstring for personalHandler /for personal accountInfo handler,make some parameter"""
    def __init__(self,access_key,secret_key):
        try:
            #个人信息
            self.account_info = HuobiService.getAccountInfo(ACCOUNT_INFO,access_key,secret_key)
            #委托单信息
            self.getOrder = HuobiService.getOrders(2,GET_ORDERS,access_key,secret_key)
            #借用的杠杆币          
            if self.account_info:
                self.available_cny_display = float(self.account_info['available_cny_display']) if self.account_info.has_key('available_cny_display') else 0
                self.loan_cny_display = float(self.account_info['loan_cny_display']) if self.account_info.has_key('loan_cny_display') else None
                self.loan_ltc_display = float(self.account_info['loan_ltc_display']) if self.account_info.has_key('loan_ltc_display') else None
                self.available_ltc_display = self.account_info['available_ltc_display']
                self.ltc_total = float(self.account_info['available_ltc_display'])+float(self.account_info['frozen_ltc_display'])
                #全部的财产
                self.total = self.account_info['total']
                #净值(即除开杠杆)
                self.net_asset = float(self.account_info['net_asset'])
            #akey
            self.a_key = access_key
            #skey
            self.s_key = secret_key
            #uid
            db = d.db_control()
            self.uid = db.select('user',access_key=self.a_key)[0][1]
            #收益
            print 
            self.profit = self.Profit()
            #当前仓位
            self.freightSpace = self.freightSpace1()
        except BaseException as e:
            self.total = 0
            self.profit = 0
            self.getOrder = {}
            self.net_asset = 0
            self.loan_ltc_display = 0
            self.available_ltc_display = 0
            print e

    @openDB
    def ProfitRate(self,db,uid):
        # db = d.db_control()
        result = db.select('SETTING',UID=uid)
        self.total_money = float(result[0][2])
        db.close()
        self.ProfitRate = '%.4f'%((self.net_asset-self.total_money)/self.total_money*100) if self.total_money !=0 else 0
        return self.ProfitRate

    @openDB
    def Profit(self,db):
        # db = d.db_control()
        setting = db.select('SETTING',UID = self.uid)
        profit = '%.2f'%(float(self.net_asset)-float(setting[0][2]))
        return profit
        
    def freightSpace1(self):
        parameter = pa.parameter()
        parameter.__init__()
        result = float_format((parameter.buyone_price*self.ltc_total)/self.net_asset)
        return result

    def CancelOrder(self,coinType,id):
        try:
            result = HuobiService.cancelOrder(coinType, id, CANCEL_ORDER, self.a_key, self.s_key)
            if result.has_key('result'):
                return result
            else:
                return {'result':'fail'}
        except BaseException as e:
            print u'cancel order detect trouble!!',e


    def BombPrice(self):
        if self.loan_ltc_display and self.total:
            bombprice = float_format((float(self.total)*100/110)/float(self.loan_ltc_display))
            return bombprice
        if self.loan_cny_display and self.total:
            bombprice = float_format(((float_format(float(self.total))-float_format(float(self.loan_cny_display)))*100/110)/float_format(float(self.ltc_total)))
            return bombprice
        return

    '''
    table:tradePenny
    column: uid      type   coin amount     price     statu msg,order_id
            self.uid,'Buy','LTC',sellCount,sellPrice, '0',  msg,result['id']
    '''

    @openDB
    def ltcBuy(self,db,buyCount,buyPrice):
        try:
            now = time.strftime(r'%Y/%m/%d %H:%M:%S',time.localtime())
            result = HuobiService.buy(2,buyPrice,buyCount,None,None,BUY,self.a_key,self.s_key)
            #msg = now + u'\n 买入价格:%s,买入数量:%s,'%(buyPrice,buyCount)
            if result:
                if result['result'] == 'success' and type(self.uid) == int:
                    #msg += u'挂买单已成功'
                    #db.insert('tradePenny',self.uid,'Buy','LTC',buyCount,buyPrice,'0',msg,result['id'])
                    result = {'statu':'success','SellPrice':buyPrice,'SellCount':buyCount}
                else:
                    #msg += u'挂买单失败'
                    #db.insert('tradePenny',self.uid,'Buy','LTC',buyCount,buyPrice,'0',msg,None)
                    result = {'statu':'fail'}
                return result
        except BaseException as e:
            print 'ltcBuy wrong.',e            

    @openDB
    def ltcSell(self,db,sellCount,sellPrice):
        try:
            now = time.strftime(r'%Y/%m/%d %H:%M:%S',time.localtime())
            result = HuobiService.sell(2,sellPrice,sellCount,None,None,SELL,self.a_key,self.s_key)
            msg = now + u' 卖出价格:%s,卖出数量:%s,'%(sellPrice,sellCount)
            if result:
                if result.has_key('result') and type(self.uid) == int:
                    msg += u'挂卖单成功'
                    db.insert('tradePenny',self.uid,'Sell','LTC',sellCount,sellPrice,'0',msg,result['id'])   
                    result = {'statu':'success','SellPrice':sellPrice,'SellCount':sellCount}
                elif result.has_key('msg'):
                    msg += u'挂卖单失败'                
                    db.insert('tradePenny',self.uid,'Sell','LTC',sellCount,sellPrice,'0',msg,None)
                    result = {'statu':'fail'}
                return result
        except BaseException as e:
            print 'ltcSell wrong.',e
            return None

    #取消订单
    @openDB
    def cancel_order(self,db,order_id):
        try:
            order_info = HuobiService.getOrderInfo(2,order_id,ORDER_INFO)
            msg = '价格:%s,数量:%s '%(order_info['order_price'],order_info['order_amount'])
            cancelResult = HuobiService.cancelOrder(2,order_id,CANCEL_ORDER)
            if cancelResult.has_key('result') and order_info:
                msg += '取消订单成功'
            else:
                msg += '取消订单失败'
            db.insert('tradePenny',time.strftime('%Y%m%d%H%M%S',time.localtime()),self.uid,msg)
        except BaseException as e:
            print 'ltcCancel wrong.',e
            

    #取消全部订单
    @openDB
    def cancel_allorders(self,db):
        try:
            getOrder = HuobiService.getOrders(2,GET_ORDERS,self.a_key,self.s_key)
            for order in getOrder:
                self.cancel_order(order['id'])
            msg = '取消全部订单成功.'
            db.insert('tradePenny',time.strftime('%Y%m%d%H%M%S',time.localtime()),self.uid,msg)
        except BaseException as e:
            print 'ltcCancelALL wrong.',e

    #写入最新的止损价
    @openDB
    def liquidation_price(self,db):
        try:
            net_asset = (HuobiService.getAccountInfo(ACCOUNT_INFO))['net_asset']
        except BaseException as e:
            print u'method_collection:暂时无法获取总量',e
        #判断是否能获取到net_asset
        if 'net_asset' in dir():
            coefficient = db.select('SETTING',UID=self.uid)[0][6]
            try:
                db.insert('SETTING',TESTMONEY = (float_format(net_asset)*float_format(coefficient)))
            except BaseException as e:
                print u'liquidation price wrong,',e
                return

    @openDB
    def dealOrder(self,db):
        try:
            dealOrders = (HuobiService.getNewDealOrders(2,NEW_DEAL_ORDERS,self.a_key,self.s_key))
        except BaseException as e:
            print u'PH dealOrder:无法获取最近成交单',e
            dealOrders = None
        DBdealOrders = db.select('dealOrder',uid=self.uid)
        resultOrder = []
        collectOrderId = []
        if dealOrders:
            dealOrders.sort(key=lambda i:float(i['last_processed_time']))
            if DBdealOrders:
                for order in dealOrders:
                    collectOrderId.append(order['id'])
                    #数据库表里的第一条数据的order_id跟新获取的数据做比对
                    if DBdealOrders[-1][2] == order['id']:
                        orderIndex = dealOrders.index(order)
                        if orderIndex < 9:
                            for i in range(orderIndex+1,10):
                                print dealOrders[i]
                                resultOrder.append(dealOrders[i])
                            return resultOrder
                        else:
                            return None
                if DBdealOrders[-1][2] not in collectOrderId:
                    return dealOrders
            else:
                return dealOrders
        return None    



if __name__ == '__main__':
    import sys
    default_encoding = 'utf-8'
    if sys.getdefaultencoding() != default_encoding:
        reload(sys)
        sys.setdefaultencoding(default_encoding)

    p = personalHandler('d76242eb-d39e3b03-6341baee-64707', 'ca3624e3-54cde80d-aee1edcd-e5ddd')
    p.__init__('d76242eb-d39e3b03-6341baee-64707', 'ca3624e3-54cde80d-aee1edcd-e5ddd')
    print p.freightSpace
    print p.dealOrder()