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


if __name__ == '__main__':
    db = db.db_control()
    p = p.parameter()
    #db.creatTable('SETTING','UID INTEGER PRIMARY KEY','TESTMONEY BLOB','TOTALMONEY BLOB','BUYCOUNT BLOB','overHighPrice BLOB','overLowPrice BLOB','COEFFICIENT BLOB','lastPrice BLOB','OneBuyCount integer')
    #db.insert('SETTING', 0,700,700,1,27,25,0.985,0,1)
    #db.insert('SETTING', 1,0,0,1,27,25,0.985,0,1)
    #db.delete('SETTING')
    d1 = {'PriceDict':{0:3,1:6,2:7,3:11,4:20,5:21}}
    d2 = {'UID':1}
    db.update('SETTING',d1,d2)
    d = db.select('SETTING')
    print d
