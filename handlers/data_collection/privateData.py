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
                    dbLink.insert('privateData',user[1],time.strftime('%Y%m%d%H%M%S',time.localtime()),net_asset,ProfitRate,total,bombprice)
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


