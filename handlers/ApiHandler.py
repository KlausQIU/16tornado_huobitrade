#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.web
import tornado.httpserver  
import tornado.ioloop  
import tornado.options  
import tornado.escape
import tornado.websocket
import json
import sys
import os
import tornado.ioloop
append_path =  os.path.dirname(os.getcwd())
sys.path.append(append_path)
import urllib2,json,time,threading
from datetime import datetime 
from strategy import parameter as p
from strategy import personalHandler as pH
from handlers.data_collection import db as d
from strategy import general
from tornado.concurrent import run_on_executor
import requests
from data_collection.publicData import publicDataReturn,ltcDataReturn
from handlers.data_collection import privateData


__author__ = 'KlausQiu'


class BaseWebSocketHandler(tornado.websocket.WebSocketHandler):
    def baseOpenDb(self):
        db = d.db_control()
        username = tornado.escape.utf8(self.get_secure_cookie('user'))
        return db,username

    def on_close(self):
        print "%s WebSocket closed"%self.__class__.__name__

class ProfitHandler(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print "ProfitHandler websocket open"
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        result = db.select('profitData',uid=result[0][1])
        db.close()
        if len(result) > 20:
            result = result[-200:]
        respon_json = tornado.escape.json_encode(result) 
        self.write_message(respon_json)
  
class accountInfo(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print "AccountInfo websocket open"
        self.AccountInfo = tornado.ioloop.PeriodicCallback(self.SentData, 3000)
        self.AccountInfo.start()

    def SentData(self):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        result = db.select('SETTING',UID=result[0][1])
        data = privateData.privateDataReturn(result[0][0])
        testMoney = result[0][1]
        respon = {
        'ProfitRate' : data[3],
        'testMoney' : testMoney,
        'net_asset' : data[2],
        'moneyTotal':data[4],
        'bombprice':data[5]
        }
        respon_json = tornado.escape.json_encode(respon)
        self.write_message(respon_json)

    def on_close(self):
        print "AccountInfo websocket close"
        self.AccountInfo.stop()

class APIInfo(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print 'APIInfo has been opened'
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            ACCESS_KEY=result[0][4]
            SECRET_KEY=result[0][5]
            SettingResult = db.select('SETTING',UID = result[0][1])
            result = {'access_key':ACCESS_KEY,'secret_key':SECRET_KEY,'TOTALMONEY':SettingResult[0][2]}
            respon_json = tornado.escape.json_encode(result)
            self.write_message(respon_json)

    def on_message(self, message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            selectRow = {'name':username}
            message = json.loads(message)
            UResult = db.select('user',name = username)
            userRow = {key:message[key] for key in ['access_key','secret_key']} 
            UserResult = db.update("user",userRow,selectRow)
            setRow = {key:message[key] for key in ['TOTALMONEY']}
            setselect = {'UID':UResult[0][1]}
            SetResult = db.update("SETTING",setRow,setselect)
            if UserResult['msg'] == 'success':
                respon_json = tornado.escape.json_encode({'msg':'success'})
                self.write_message(respon_json)
            else:
                result = tornado.escape.json_encode({'msg':'fail'})
                self.write_message(result)

class entrustInfo(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print "entrustInfo websocket Open"
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            personalH = pH.personalHandler(result[0][4],result[0][5])
            getOrders = personalH.getOrder
            respon_json = tornado.escape.json_encode(getOrders)
            self.write_message(respon_json)
        
class entrustCancel(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print 'cancel Order websocket Open'

    def on_message(self, message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            personalH = pH.personalHandler(result[0][4],result[0][5])
            oid = int(message)
            result = personalH.CancelOrder(2,oid)
            respon_json = tornado.escape.json_encode(result)
            self.write_message(respon_json)

class tradeSetting(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print 'tradeSetting Order websocket Open'

    def on_message(self, message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            personalH = pH.personalHandler(result[0][4],result[0][5])
            message = json.loads(message)
            selectRow = {'UID':result[0][1]}
            SettingResult = db.update("SETTING",message,selectRow)
            if SettingResult['msg'] == 'success':
                result = db.select('SETTING',UID = result[0][1])
                result = {'testMoney':result[0][1]}
                respon_json = tornado.escape.json_encode(result)
                self.write_message(respon_json)

class tradeSetInfo(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print 'tradeSetInfo Order websocket Open'
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            personalH = pH.personalHandler(result[0][4],result[0][5])
            selectRow = {'UID':result[0][1]}
            result = db.select('SETTING',UID = result[0][1])
            result = {'testMoney':result[0][1],'highPrice':result[0][4],'lowPrice':result[0][5]}
            respon_json = tornado.escape.json_encode(result)
            self.write_message(respon_json)

class dealMessage(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'dealMessage wesocket Open'
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            personalH = pH.personalHandler(result[0][4],result[0][5])
            dealOrders = personalH.DealOrder(2) if personalH.DealOrder(2) else {}
            respon_json = tornado.escape.json_encode(dealOrders)
            self.write_message(respon_json)
            self.on_close()

class avatarInfo(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'avatarInfo websocket Open'
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            avatarInfo = {"name":result[0][2],"password":result[0][3]}
            respon_json = tornado.escape.json_encode(avatarInfo)
            self.write_message(respon_json)
            self.on_close()

    def on_message(self, message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            message = json.loads(message)
            userRow = {'name':message['name'],'password':message['password']}
            selectRow = {'UID':result[0][1]}
            UserResult = db.update("user",userRow,selectRow)
            if UserResult['msg'] == 'success':
                respon_json = tornado.escape.json_encode(userRow)
                self.write_message(respon_json)
            else:
                result = tornado.escape.json_encode({'msg':'fail'})
                self.write_message(result)
                self.on_close()

class gridSetApi(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'gridSetApi websocket Open'

    def on_message(self,message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            message = json.loads(message)
            message = ','.join(message)
            updateRow = {'position':message}
            selectRow = {'UID':result[0][1]}
            FResult = db.update("fibonacciGrid",updateRow,selectRow)
            if FResult['msg'] == 'success':
                respon_json = tornado.escape.json_encode(FResult)
                self.write_message(respon_json)
                self.on_close()
            else:
                result = tornado.escape.json_encode({'msg':'fail'})
                self.write_message(result)
                self.on_close()

class tradePennySetHandler(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'tradePennySetHandler websocket Open'

    def on_message(self,message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            message = json.loads(message)
            print message
            updateRow = message
            selectRow = {'UID':result[0][1]}
            SResult = db.update("SETTING",updateRow,selectRow)
            print SResult
            if SResult['msg'] == 'success':
                respon_json = tornado.escape.json_encode(SResult)
                self.write_message(respon_json)
                self.on_close()
            else:
                result = tornado.escape.json_encode({'msg':'fail'})
                self.write_message(result)
                self.on_close()
        
class tradeOrderSetHandler(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'tradeOrderSetHandler websocket Open'

    def on_message(self,message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            message = json.loads(message)
            print message
            updateRow = {'PriceDict':str(message)}
            selectRow = {'UID':result[0][1]}
            SResult = db.update("SETTING",updateRow,selectRow)
            print SResult
            if SResult['msg'] == 'success':
                respon_json = tornado.escape.json_encode(SResult)
                self.write_message(respon_json)
                self.on_close()
            else:
                result = tornado.escape.json_encode({'msg':'fail'})
                self.write_message(result)
                self.on_close()

class tradePennyShow(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'tradePennyShow websocket Open'

    def on_message(self,message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            message = json.loads(message)
            print message
            updateRow = {'PriceDict':str(message)}
            selectRow = {'UID':result[0][1]}
            SResult = db.update("SETTING",updateRow,selectRow)
            print SResult
            if SResult['msg'] == 'success':
                respon_json = tornado.escape.json_encode(SResult)
                self.write_message(respon_json)
                self.on_close()
            else:
                result = tornado.escape.json_encode({'msg':'fail'})
                self.write_message(result)
                self.on_close()

class coinDataHandler(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'coinDataHandler websocket Open'
        self.coinData = tornado.ioloop.PeriodicCallback(self.SentData, 3000)
        self.coinData.start()

    def SentData(self):
        ltc = requests.get(r'http://api.huobi.com/staticmarket/ticker_ltc_json.js')
        ticker_ltc = json.loads(ltc.text)
        ltc.close()
        btc = requests.get(r'http://api.huobi.com/staticmarket/ticker_btc_json.js')
        ticker_btc = json.loads(btc.text)
        btc.close()
        message = {"ltc":ticker_ltc,"btc":ticker_btc}
        respon_json = tornado.escape.json_encode(message)
        self.write_message(respon_json)

    def on_close(self):
        print "coinDataHandler websocket close"
        self.coinData.stop()


class handlerltcHandler(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'handlerltcHandler websocket Open'
        self.handlerltc = tornado.ioloop.PeriodicCallback(self.SentData, 5000)
        self.handlerltc.start()

    def SentData(self):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        result = db.select('profitData',uid=result[0][1])
        db.close()
        if len(result) > 20:
            result = result[-200:]
            xAxisData = [item[1][8:10]+':'+item[1][10:12] for item in result]
            showdata = [item[4] for item in result]
        data = ltcDataReturn()
        xBxisData = eval(data['xBxisData'])
        ltcData = eval(data['ltcData'])
        respon_json = tornado.escape.json_encode({"xBxisData":xBxisData,"ltcData":ltcData,"xAxisData":xAxisData,"showdata":showdata}) 
        self.write_message(respon_json)

    def on_close(self):
        print "handlerltcHandler websocket close"
        self.handlerltc.stop()

class PublicDealMessage(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'PublicDealMessage websocket Open'
        
    def on_message(self, message):
        self.DealMessage = tornado.ioloop.PeriodicCallback(self.SentData, 1000)
        self.DealMessage.start()
    
    def SentData(self):
        data = publicDataReturn()
        PublicDealMessage = general.judgeData(eval(data['dealdata']))
        if PublicDealMessage:
            respon_json = tornado.escape.json_encode({'PublicDealMessage':PublicDealMessage,"ltc":data['ticker_ltc'],"btc":data['ticker_btc'],'ltcTradeVol':data['ltcTradeVol']})
            self.write_message(respon_json,binary=False)

    def on_close(self):
        print 'PublicDealMessage websocket Closed'
        self.DealMessage.stop()

class DrawProfit(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'DrawProfit websocket Open'
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        result = db.select('profitData',uid=result[0][1])
        if len(result) > 3000:
            result = result[-3000:]
            xAxisData = [item[1][4:8]+'/'+item[1][8:10]+':'+item[1][10:12] for item in result]
            showdata = [item[4] for item in result]
        respon_json = tornado.escape.json_encode({"xAxisData":xAxisData,"showdata":showdata}) 
        self.write_message(respon_json)

    def on_close(self):
        print "DrawProfit websocket close"


class HuobiLtcSell(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'HuobiLtcSell WebSocket Open'
        db,username = self.baseOpenDb()
        result = db.select('user',name= username)
        if result:
            if len(result[0][4]) == 32 and len(result[0][5]) == 32:
                personalH = pH.personalHandler(result[0][4],result[0][5])
                available_ltc_display = personalH.available_ltc_display
                data = publicDataReturn()
                tradePrice = data['ticker_ltc'] if data else 0
                respon_json = tornado.escape.json_encode({"available_ltc_display":available_ltc_display,"tradePrice":tradePrice})
                self.write_message(respon_json)
            else:
                respon_json = tornado.escape.json_encode({"available_ltc_display":0,"tradePrice":0})
                self.write_message(respon_json)

    def on_message(self,message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            message = json.loads(message)
            print message
            personalH = pH.personalHandler(result[0][4],result[0][5])
            ltcSellResult = personalH.ltcSell(message['SellCount'],message['SellPrice'])
            if ltcSellResult:
                if ltcSellResult['statu'] == 'success':
                    respon_json = tornado.escape.json_encode({'msg':'success'})
                    self.write_message(respon_json)
                else:
                    respon_json = tornado.escape.json_encode({'msg':'fail'})
                    self.write_message(respon_json)
            else:
                respon_json = tornado.escape.json_encode({'msg':'fail'})
                self.write_message(respon_json)

    #只是测试
 






