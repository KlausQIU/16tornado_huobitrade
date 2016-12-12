#!/usr/bin/env python
# coding:utf-8

import tornado.web
import db 
import os
import sys
import time
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from strategy import parameter as p
from strategy.setting import total_money
from strategy import personalHandler as pH
import requests
import json
import time
import sqlite3
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

__author__ = 'klausQiu'

def main():
    while True:
        print 'enter privateDataCollection'
        dbLink = db.db_control()
        users = dbLink.select('user')
        print users
        for user in users:
            if len(user[4]) == 32 and len(user[5]) == 32:
                now = datetime.now()
                print 'now:',now.strftime('%Y%m%d-%H:%M')
                try:
                    personalH = pH.personalHandler(user[4],user[5])
                    ProfitRate = personalH.ProfitRate(user[1])
                    net_asset = personalH.net_asset
                    total = personalH.total
                    bombprice = personalH.BombPrice()
                    str_now = time.strftime('%Y%m%d%H%M%S',time.localtime())
                    dbLink.insert('privateData',user[1],str_now,net_asset,ProfitRate,total,bombprice)
                    dealOrders = personalH.dealOrder()
                    if dealOrders:
                        print dealOrders
                        for order in dealOrders:
                            # 'uid BLOB','time BLOB','order_id integer','order_time BLOB','last_processed_time BLOB','order_amount BLOB','order_price BLOB','type BLOB'
                            now = time.strftime(r'%Y/%m/%d %H:%M:%S',time.localtime())
                            msg = now
                            msg +=  u'  卖出' if int(order['type']) == 2 else u'  买入'
                            msg += u'  已成交  %s   %s'%(order['order_price'],order['order_amount'])
                            print msg
                            dbLink.insert('dealOrder',user[1],str_now,order['id'],order['order_time'],order['last_processed_time'],order['order_amount'],order['order_price'],order['type'],msg)
                            # 'tradePenny','uid integer','BuyOrSell BLOB','Coin Blob','Amount BLOB','Price BLOB','Status Blob','msg BLOB','order_id BLOB'
                except BaseException as e:
                    print u'huobi api fxcking shit again!',e
        privateData = dbLink.select('privateData')
        count = len(dbLink.select('privateData')) if privateData else 0
        if count >= 50:
            dbLink.delete('privateData',Time=(min(dbLink.select('privateData')))[0])
        time.sleep(3)


def privateDataReturn(uid):
    dbLink = db.db_control()
    data = dbLink.select('privateData',uid=uid)
    if data:
        return data[-1]
    return


if __name__ == '__main__':
    while True:
        main()
        time.sleep(3)


